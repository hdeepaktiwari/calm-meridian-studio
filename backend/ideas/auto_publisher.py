"""
Auto Publisher - Autonomous agent that generates and publishes Shorts on schedule.
US-optimized schedule: 7:00 AM EST & 9:30 PM EST daily.
"""
import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from domains import DOMAIN_REGISTRY
from ideas.idea_bank import IdeaBank
from ideas.calendar import ContentCalendar

EST = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

SCHEDULE_FILE = Path("publish_schedule.json")
AUTOPUBLISH_STATE_FILE = Path("autopublish_state.json")

# Daily publish times in EST (hour, minute)
PUBLISH_TIMES = [(7, 0), (21, 30)]


def _load_state() -> dict:
    if AUTOPUBLISH_STATE_FILE.exists():
        try:
            with open(AUTOPUBLISH_STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"enabled": False, "published_slots": []}


def _save_state(state: dict):
    with open(AUTOPUBLISH_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


class AutoPublisher:
    """Autonomous agent that generates and publishes Shorts on schedule."""

    def __init__(self):
        self.idea_bank = IdeaBank()
        self.calendar = ContentCalendar()

    def is_enabled(self) -> bool:
        return _load_state().get("enabled", False)

    def toggle(self) -> bool:
        state = _load_state()
        state["enabled"] = not state.get("enabled", False)
        _save_state(state)
        return state["enabled"]

    def get_status(self) -> dict:
        state = _load_state()
        stats = self.idea_bank.get_stats()
        return {
            "enabled": state.get("enabled", False),
            "next_slots": self.get_next_publish_slots(7),
            "idea_bank_health": "good" if stats["available"] > 20 else "low" if stats["available"] > 10 else "critical",
            "ideas_available": stats["available"],
        }

    def get_next_publish_slots(self, count: int = 7) -> list:
        now = datetime.now(EST)
        slots = []
        current_date = now.date()

        while len(slots) < count:
            for hour, minute in PUBLISH_TIMES:
                slot_time = datetime(current_date.year, current_date.month, current_date.day,
                                     hour, minute, tzinfo=EST)
                if slot_time > now:
                    slots.append({
                        "time_est": slot_time.strftime("%Y-%m-%d %I:%M %p EST"),
                        "time_utc": slot_time.astimezone(UTC).isoformat(),
                        "day": slot_time.strftime("%A"),
                    })
                    if len(slots) >= count:
                        break
            current_date += timedelta(days=1)

        return slots

    def _slot_key(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d_%H:%M")

    def _is_slot_done(self, slot_time: datetime) -> bool:
        state = _load_state()
        key = self._slot_key(slot_time)
        return key in state.get("published_slots", [])

    def _mark_slot_done(self, slot_time: datetime):
        state = _load_state()
        key = self._slot_key(slot_time)
        if "published_slots" not in state:
            state["published_slots"] = []
        state["published_slots"].append(key)
        # Keep only last 60 entries
        state["published_slots"] = state["published_slots"][-60:]
        _save_state(state)

    async def run_scheduled_publish(self):
        """Called by scheduler. Checks if it's time to publish."""
        if not self.is_enabled():
            return

        now = datetime.now(EST)

        # Check if idea bank is low, auto-generate
        stats = self.idea_bank.get_stats()
        if stats["available"] < 10:
            print("📦 Idea bank low, generating 100 more ideas...")
            try:
                await self.idea_bank.generate_ideas(100)
            except Exception as e:
                print(f"❌ Idea generation failed: {e}")

        # Check each publish time for today
        for hour, minute in PUBLISH_TIMES:
            slot_time = datetime(now.year, now.month, now.day, hour, minute, tzinfo=EST)
            # Start 15 min before publish time, window is 15 min before to 30 min after
            window_start = slot_time - timedelta(minutes=15)
            window_end = slot_time + timedelta(minutes=30)

            if window_start <= now <= window_end and not self._is_slot_done(slot_time):
                idea = self.idea_bank.pick_idea()
                if idea:
                    print(f"🎬 Auto-publishing for slot {slot_time.strftime('%I:%M %p EST')}: {idea['title']}")
                    try:
                        await self.generate_and_publish(idea, slot_time)
                        self._mark_slot_done(slot_time)
                    except Exception as e:
                        print(f"❌ Auto-publish failed: {e}")
                        # Log failure to calendar
                        self.calendar.add_entry({
                            "date": slot_time.strftime("%Y-%m-%d"),
                            "time": slot_time.strftime("%I:%M %p EST"),
                            "type": "short",
                            "domain": idea.get("domain", "Unknown"),
                            "title": idea.get("title", ""),
                            "status": "failed",
                            "hook_line": idea.get("hook_line", ""),
                            "error": str(e),
                        })
                        self._mark_slot_done(slot_time)

    async def generate_and_publish(self, idea: dict, publish_time: datetime):
        """Generate a Short from an idea and schedule YouTube upload."""
        from core.shorts_generator import ShortsGenerator

        SHORTS_VIDEOS_DIR = Path("generated_shorts")
        SHORTS_VIDEOS_DIR.mkdir(exist_ok=True)

        domain = DOMAIN_REGISTRY.get(idea["domain"])
        if not domain:
            raise ValueError(f"Unknown domain: {idea['domain']}")

        # Add calendar entry as generating
        cal_entry = self.calendar.add_entry({
            "date": publish_time.strftime("%Y-%m-%d"),
            "time": publish_time.strftime("%I:%M %p EST"),
            "type": "short",
            "domain": idea["domain"],
            "title": idea["title"],
            "status": "generating",
            "hook_line": idea.get("hook_line", ""),
        })

        try:
            gen = ShortsGenerator()
            folder_name = f"{domain.name.replace(' ', '')}_{45}s_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            project_folder = SHORTS_VIDEOS_DIR / folder_name
            project_folder.mkdir(parents=True, exist_ok=True)

            loop = asyncio.get_event_loop()
            output_path, scene_data, seo = await loop.run_in_executor(
                None,
                lambda: gen.generate_short(
                    domain=domain,
                    target_duration=45,
                    project_folder=project_folder,
                    progress_callback=lambda pct, msg: print(f"  [{pct}%] {msg}"),
                ),
            )

            # Upload to YouTube with scheduled publish time
            youtube_url = None
            try:
                from utils.youtube_upload import upload_video as yt_upload_video
                # Convert publish_time to UTC for YouTube
                publish_utc = publish_time.astimezone(UTC)
                result = yt_upload_video(
                    video_path=str(output_path),
                    title=seo.get("title", idea["title"]),
                    description=seo.get("description", idea["description"]),
                    tags=seo.get("tags", []),
                    privacy="private",
                    publish_at=publish_utc.isoformat(),
                )
                youtube_url = result.get("url") if isinstance(result, dict) else None
            except Exception as e:
                print(f"⚠️ YouTube upload failed: {e}")

            # Mark idea as used
            self.idea_bank.mark_used(idea["id"], cal_entry["id"])

            # Update calendar entry
            youtube_id = result.get("video_id") if isinstance(result, dict) else None
            self.calendar.update_entry(cal_entry["id"],
                status="published" if youtube_url else "scheduled",
                youtube_url=youtube_url or "",
                youtube_id=youtube_id or "",
                video_path=str(output_path),
                duration=scene_data.get("duration", 45),
            )

            print(f"✅ Published: {idea['title']}")

        except Exception as e:
            self.calendar.update_entry(cal_entry["id"], status="failed", error=str(e))
            raise

    def get_publish_calendar(self, year: int, month: int) -> dict:
        entries = self.calendar.get_month(year, month)
        by_date = {}
        for e in entries:
            d = e.get("date", "")
            if d not in by_date:
                by_date[d] = []
            by_date[d].append(e)
        return by_date
