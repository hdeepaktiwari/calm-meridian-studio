"""
Autonomous Long-Form Video Publisher.
Generates and publishes 1 long-form video per day, maintaining a 2-day buffer
of scheduled videos on YouTube.
"""
import json
import uuid
import random
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
STATE_FILE = Path("longform_publish_state.json")


class LongFormPublisher:
    """Autonomous long-form video publisher. Generates 1 video/day."""

    def _load_state(self) -> dict:
        defaults = {
            "enabled": True,
            "last_generated": None,
            "last_published": None,
        }
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE) as f:
                    state = json.load(f)
                for k, v in defaults.items():
                    state.setdefault(k, v)
                return state
            except Exception:
                pass
        # Create default state file
        self._save_state(defaults)
        return defaults

    def _save_state(self, state: dict):
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2, default=str)

    def is_enabled(self) -> bool:
        return self._load_state().get("enabled", True)

    def toggle(self) -> bool:
        state = self._load_state()
        state["enabled"] = not state.get("enabled", True)
        self._save_state(state)
        return state["enabled"]

    async def check_and_publish(self):
        """Called by scheduler. Check buffer and generate if needed."""
        if not self.is_enabled():
            return

        # Check how many days of buffer we have
        days_buffer = await self._get_days_of_buffer()
        print(f"[LONGFORM] Buffer: {days_buffer} days")

        if days_buffer >= 2:
            print("[LONGFORM] Buffer adequate, skipping generation")
            return

        print(f"[LONGFORM] Buffer low ({days_buffer} days), generating new video...")
        try:
            job = await self.generate_one_video()
            if job and job.get("video_path"):
                result = await self.publish_video(job)
                state = self._load_state()
                state["last_generated"] = datetime.now(IST).isoformat()
                state["last_published"] = datetime.now(IST).isoformat()
                self._save_state(state)
                print(f"[LONGFORM] Published: {result.get('url', 'unknown')}")
        except Exception as e:
            print(f"[LONGFORM] Generation/publish error: {e}")
            import traceback
            traceback.print_exc()

    async def _get_days_of_buffer(self) -> int:
        """Query YouTube for scheduled videos and calculate buffer days."""
        try:
            from utils.youtube_upload import _get_youtube_service, _get_scheduled_slots
            youtube = _get_youtube_service()
            taken_dates = _get_scheduled_slots(youtube)
            if not taken_dates:
                return 0
            today = datetime.now(IST).date()
            future_dates = [
                d for d in taken_dates
                if datetime.strptime(d, "%Y-%m-%d").date() >= today
            ]
            if not future_dates:
                return 0
            last_date = max(
                datetime.strptime(d, "%Y-%m-%d").date() for d in future_dates
            )
            return (last_date - today).days
        except Exception as e:
            print(f"[LONGFORM] Buffer check error: {e}")
            return 0

    async def generate_one_video(self) -> dict:
        """Generate a single long-form video using round-robin domain."""
        from domains import DOMAIN_REGISTRY
        from core.video_generator import VideoGenerator
        from utils.file_manager import FileManager
        from utils.auto_prompt import generate_auto_prompt
        # Import state management from main
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from main import (
            load_automation_state, save_automation_state,
            load_music_library, MUSIC_DIR, VIDEOS_DIR,
        )

        state = load_automation_state()
        domain_names = list(DOMAIN_REGISTRY.keys())
        library = load_music_library()

        base_durations = [180, 300]

        # Pick domain via round-robin
        domain_name = domain_names[state["domain_index"] % len(domain_names)]
        domain = DOMAIN_REGISTRY[domain_name]

        # Duration with variation
        base_dur = base_durations[
            state.get("duration_toggle", 0) % len(base_durations)
        ]
        dur = base_dur + random.randint(5, 45)

        # Music
        if dur <= 225:
            music_pool = library.get("short", [])
        else:
            music_pool = library.get("long", [])
        music_track = (
            music_pool[state["music_index"] % len(music_pool)]
            if music_pool else None
        )
        music_path = (
            str(MUSIC_DIR / music_track["filename"]) if music_track else None
        )

        # Auto-prompt
        custom_desc = generate_auto_prompt(domain, dur)

        # Update state
        state["domain_index"] = state.get("domain_index", 0) + 1
        state["duration_toggle"] = state.get("duration_toggle", 0) + 1
        state["music_index"] = state.get("music_index", 0) + 1
        state["total_generated"] = state.get("total_generated", 0) + 1
        save_automation_state(state)

        # Generate
        file_manager = FileManager("generated_videos")
        video_gen = VideoGenerator()
        project_folder = file_manager.create_project_folder(domain.name, dur)

        print(f"[LONGFORM] Generating: {domain_name}, {dur}s")

        loop = asyncio.get_event_loop()
        output_path, scenes, seo_metadata = await loop.run_in_executor(
            None,
            lambda: video_gen.generate_video(
                domain=domain,
                duration=dur,
                custom_description=custom_desc,
                audio_path=music_path,
                project_folder=project_folder,
                use_domain_weights=True,
                include_signature=True,
                optimize_lighting=True,
                progress_callback=lambda pct, msg: print(
                    f"  [LONGFORM {pct}%] {msg}"
                ),
            ),
        )

        file_manager.save_metadata(project_folder, domain, dur, scenes, None)

        return {
            "video_path": str(output_path),
            "project_folder": str(project_folder),
            "domain": domain_name,
            "duration": dur,
            "seo_metadata": seo_metadata,
            "scenes": scenes,
            "music_name": music_track["name"] if music_track else None,
        }

    async def publish_video(self, job: dict) -> dict:
        """Upload generated video to YouTube with auto-scheduling."""
        from utils.youtube_upload import upload_video as yt_upload_video
        from utils.thumbnail_generator import generate_thumbnail
        from ideas.calendar import ContentCalendar

        video_path = job["video_path"]
        project_folder = Path(job["project_folder"])
        seo = job.get("seo_metadata", {})

        title = seo.get("title", job.get("domain", "Calm Meridian"))
        description = seo.get("description", "")
        tags = seo.get("tags", [])

        # Generate thumbnail
        images_dir = project_folder / "images"
        thumb_path = project_folder / "thumbnail.jpg"
        thumb = None
        if images_dir.exists():
            generate_thumbnail(title, str(images_dir), str(thumb_path))
            thumb = str(thumb_path)

        # Upload with auto-scheduling
        result = yt_upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy="public",
            thumbnail_path=thumb,
            schedule=True,
        )

        # Save youtube info
        yt_info = {
            "video_id": result["video_id"],
            "url": result["url"],
            "published_at": datetime.now(IST).isoformat(),
            "scheduled_at": result.get("scheduled_at"),
            "title": title,
        }
        with open(project_folder / "youtube_info.json", "w") as f:
            json.dump(yt_info, f, indent=2)

        # Log to content calendar
        calendar = ContentCalendar()
        scheduled_at = result.get("scheduled_at", "")
        # Parse scheduled date
        cal_date = datetime.now(IST).strftime("%Y-%m-%d")
        if scheduled_at:
            try:
                dt = datetime.fromisoformat(
                    scheduled_at.replace(".0Z", "+00:00")
                )
                cal_date = dt.astimezone(IST).strftime("%Y-%m-%d")
            except Exception:
                pass

        calendar.add_entry({
            "date": cal_date,
            "time": "8:00 AM IST",
            "type": "long",
            "domain": job.get("domain", ""),
            "title": title,
            "status": "scheduled",
            "youtube_url": result["url"],
            "video_path": video_path,
            "scheduled_at": scheduled_at,
        })

        return result

    def get_status(self) -> dict:
        state = self._load_state()
        return {
            "enabled": state.get("enabled", True),
            "last_generated": state.get("last_generated"),
            "last_published": state.get("last_published"),
            "days_of_buffer": None,  # Computed async, not available sync
        }
