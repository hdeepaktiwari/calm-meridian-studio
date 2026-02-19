"""
Cinematic Video Studio API
FastAPI backend for video generation
"""
import os
import uuid
import json
import shutil
import asyncio
import httpx
import random
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from domains import DOMAIN_REGISTRY
from core.video_generator import VideoGenerator
from utils.file_manager import FileManager
from utils.youtube_upload import upload_video as yt_upload_video, set_thumbnail as yt_set_thumbnail
from utils.thumbnail_generator import generate_thumbnail
from utils.auto_prompt import generate_auto_prompt

# Job storage with persistence
JOBS_FILE = Path("jobs_store.json")
jobs: Dict[str, Dict[str, Any]] = {}

# SSE subscribers
sse_subscribers: List[asyncio.Queue] = []

def load_jobs():
    global jobs
    if JOBS_FILE.exists():
        try:
            with open(JOBS_FILE) as f:
                jobs = json.load(f)
        except Exception:
            jobs = {}

def save_jobs():
    try:
        with open(JOBS_FILE, "w") as f:
            json.dump(jobs, f, indent=2, default=str)
    except Exception:
        pass

def update_job(job_id: str, **kwargs):
    """Update a job and notify SSE subscribers."""
    if job_id in jobs:
        jobs[job_id].update(kwargs)
        save_jobs()
        # Notify all SSE subscribers
        event_data = json.dumps(jobs[job_id], default=str)
        for q in sse_subscribers:
            try:
                q.put_nowait({"event": "job_update", "data": event_data})
            except asyncio.QueueFull:
                pass

def broadcast_sse(event: str, data: Any):
    """Broadcast an SSE event to all subscribers."""
    event_data = json.dumps(data, default=str)
    for q in sse_subscribers:
        try:
            q.put_nowait({"event": event, "data": event_data})
        except asyncio.QueueFull:
            pass

# Create directories
VIDEOS_DIR = Path("generated_videos")
VIDEOS_DIR.mkdir(exist_ok=True)
MUSIC_DIR = Path("music")
MUSIC_LIBRARY_FILE = MUSIC_DIR / "music_library.json"

AUTOMATION_STATE_FILE = Path("automation_state.json")

def load_automation_state():
    defaults = {"domain_index": 0, "duration_toggle": 0, "music_index": 0, "total_generated": 0}
    if AUTOMATION_STATE_FILE.exists():
        with open(AUTOMATION_STATE_FILE) as f:
            state = json.load(f)
        # Normalize: duration_index → duration_toggle
        if "duration_index" in state and "duration_toggle" not in state:
            state["duration_toggle"] = state.pop("duration_index")
        for k, v in defaults.items():
            state.setdefault(k, v)
        return state
    return defaults

def save_automation_state(state):
    with open(AUTOMATION_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_music_library():
    if MUSIC_LIBRARY_FILE.exists():
        with open(MUSIC_LIBRARY_FILE) as f:
            return json.load(f)
    return {"short": [], "long": []}

from ideas.idea_bank import IdeaBank
from ideas.calendar import ContentCalendar
from ideas.auto_publisher import AutoPublisher

idea_bank = IdeaBank()
content_calendar = ContentCalendar()
auto_publisher = AutoPublisher()

_scheduler_task = None

async def _autopublish_scheduler():
    """Background scheduler that checks every 30 minutes for publishing."""
    while True:
        try:
            await auto_publisher.run_scheduled_publish()
        except Exception as e:
            print(f"⚠️ Scheduler error: {e}")
        await asyncio.sleep(30 * 60)  # 30 minutes

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler_task
    load_jobs()
    # Mark any running jobs as interrupted on startup
    for jid, job in jobs.items():
        if job.get("status") == "running":
            job["status"] = "failed"
            job["error"] = "Server restarted during generation"
            job["message"] = "Interrupted by server restart"
    save_jobs()
    _scheduler_task = asyncio.create_task(_autopublish_scheduler())
    print("🎬 Cinematic Video Studio API starting...")
    print("📅 Auto-publish scheduler started (every 30 min)")
    yield
    if _scheduler_task:
        _scheduler_task.cancel()
    save_jobs()
    print("👋 Shutting down...")

app = FastAPI(
    title="Cinematic Video Studio API",
    description="AI-powered cinematic video generation",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/videos", StaticFiles(directory="generated_videos"), name="videos")

# ============== Models ==============

class DomainInfo(BaseModel):
    name: str
    icon: str
    description: str
    locations: list[str]
    signature_elements: list[str]
    color_palette: list[str]
    mood_keywords: list[str]

class PublishRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: list[str] = []
    privacy: str = 'public'

class GenerateRequest(BaseModel):
    domain: str
    duration: int
    custom_description: Optional[str] = ""
    music_id: Optional[str] = None

class BulkPublishRequest(BaseModel):
    video_ids: list[str]
    privacy: str = 'public'

class MusicTrack(BaseModel):
    id: str
    name: str
    filename: str
    duration_seconds: int
    duration_display: str
    mood: str
    instruments: list[str]
    recommended_for: list[str]

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    domain: Optional[str] = None
    duration: Optional[int] = None
    created_at: str
    completed_at: Optional[str] = None
    video_path: Optional[str] = None
    video_url: Optional[str] = None
    scenes: Optional[list] = None
    seo_metadata: Optional[dict] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: str

# ============== SSE Endpoint ==============

@app.get("/api/events")
async def sse_events(request: Request):
    """Server-Sent Events endpoint for real-time job updates."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    sse_subscribers.append(queue)

    async def event_generator():
        try:
            # Send initial state
            yield f"event: init\ndata: {json.dumps({'jobs': list(jobs.values())}, default=str)}\n\n"
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"event: {msg['event']}\ndata: {msg['data']}\n\n"
                except asyncio.TimeoutError:
                    yield f"event: ping\ndata: {{}}\n\n"
        finally:
            if queue in sse_subscribers:
                sse_subscribers.remove(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

# ============== API Endpoints ==============

@app.get("/")
async def root():
    return {
        "name": "Cinematic Video Studio API",
        "version": "2.0.0",
        "status": "running",
    }

@app.get("/api/domains", response_model=Dict[str, DomainInfo])
async def get_domains():
    result = {}
    for name, domain in DOMAIN_REGISTRY.items():
        result[name] = DomainInfo(
            name=domain.name,
            icon=domain.icon,
            description=domain.description,
            locations=domain.locations[:5],
            signature_elements=domain.signature_elements[:5],
            color_palette=domain.color_palette,
            mood_keywords=domain.mood_keywords
        )
    return result

@app.get("/api/domains/{domain_name}")
async def get_domain(domain_name: str):
    if domain_name not in DOMAIN_REGISTRY:
        raise HTTPException(status_code=404, detail={"error": "not_found", "detail": "Domain not found", "code": "DOMAIN_NOT_FOUND"})
    domain = DOMAIN_REGISTRY[domain_name]
    return {
        "name": domain.name, "icon": domain.icon, "description": domain.description,
        "locations": domain.locations, "signature_elements": domain.signature_elements,
        "lighting_conditions": domain.lighting_conditions, "color_palette": domain.color_palette,
        "mood_keywords": domain.mood_keywords
    }

# ============== Music Endpoints ==============

@app.get("/api/music")
async def get_music_library():
    library = load_music_library()
    return {
        "short": library.get("short", []),
        "long": library.get("long", []),
        "total": len(library.get("short", [])) + len(library.get("long", []))
    }

@app.get("/api/music/for-duration/{duration}")
async def get_music_for_duration(duration: int):
    library = load_music_library()
    if duration <= 225:
        tracks = library.get("short", [])
        category = "short"
    else:
        tracks = library.get("long", [])
        category = "long"
    return {"category": category, "video_duration": duration, "tracks": tracks}

@app.get("/api/music/{music_id}")
async def get_music_track(music_id: str):
    library = load_music_library()
    for track in library.get("short", []) + library.get("long", []):
        if track["id"] == music_id:
            track["url"] = f"/music/{track['filename']}"
            return track
    raise HTTPException(status_code=404, detail="Music track not found")

app.mount("/music", StaticFiles(directory="music"), name="music")

# ============== Generation ==============

@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    if request.domain not in DOMAIN_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid domain: {request.domain}")

    # Allow base durations or anything in reasonable range (3-12 min)
    if request.duration < 120 or request.duration > 720:
        raise HTTPException(status_code=400, detail="Duration must be between 120 and 720 seconds")

    music_path = None
    music_name = None
    if request.music_id:
        library = load_music_library()
        for track in library.get("short", []) + library.get("long", []):
            if track["id"] == request.music_id:
                music_path = str(MUSIC_DIR / track["filename"])
                music_name = track["name"]
                break
        if not music_path:
            raise HTTPException(status_code=400, detail=f"Music track not found: {request.music_id}")

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        "job_id": job_id, "status": "pending", "progress": 0,
        "message": "Queued for processing", "domain": request.domain,
        "duration": request.duration, "custom_description": request.custom_description,
        "music_id": request.music_id, "music_path": music_path, "music_name": music_name,
        "created_at": datetime.now().isoformat(), "completed_at": None,
        "video_path": None, "video_url": None, "scenes": None,
        "seo_metadata": None, "error": None
    }
    save_jobs()
    broadcast_sse("job_created", jobs[job_id])

    background_tasks.add_task(run_generation, job_id)
    return {"job_id": job_id, "status": "pending", "message": "Video generation started"}

async def run_generation(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return
    # Skip if cancelled
    if job.get("status") == "cancelled":
        return

    try:
        update_job(job_id, status="running", message="Initializing...")

        domain = DOMAIN_REGISTRY[job["domain"]]
        duration = job["duration"]
        custom_description = job.get("custom_description", "")
        music_path = job.get("music_path")

        file_manager = FileManager("generated_videos")
        video_gen = VideoGenerator()
        project_folder = file_manager.create_project_folder(domain.name, duration)

        def progress_callback(percent, message):
            update_job(job_id, progress=percent, message=message)

        loop = asyncio.get_event_loop()
        output_path, scenes, seo_metadata = await loop.run_in_executor(
            None,
            lambda: video_gen.generate_video(
                domain=domain, duration=duration, custom_description=custom_description,
                audio_path=music_path, project_folder=project_folder,
                use_domain_weights=True, include_signature=True,
                optimize_lighting=True, progress_callback=progress_callback
            )
        )

        file_manager.save_metadata(project_folder, domain, duration, scenes, None)

        update_job(job_id,
            status="completed", progress=100, message="Video generation complete!",
            completed_at=datetime.now().isoformat(), video_path=str(output_path),
            video_url=f"/videos/{project_folder.name}/final_video.mp4",
            scenes=scenes, seo_metadata=seo_metadata
        )

    except Exception as e:
        update_job(job_id, status="failed", error=str(e), message=f"Error: {str(e)}")

# ============== Jobs ==============

@app.get("/api/jobs")
async def list_jobs():
    return {"jobs": list(jobs.values())}

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    del jobs[job_id]
    save_jobs()
    broadcast_sse("job_deleted", {"job_id": job_id})
    return {"message": "Job deleted"}

@app.post("/api/jobs/{job_id}/retry")
async def retry_job(job_id: str, background_tasks: BackgroundTasks):
    """Retry a failed job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs[job_id]
    if job["status"] not in ("failed",):
        raise HTTPException(status_code=400, detail="Only failed jobs can be retried")

    update_job(job_id, status="pending", progress=0, message="Queued for retry",
               error=None, completed_at=None, video_path=None, video_url=None,
               scenes=None, seo_metadata=None)

    background_tasks.add_task(run_generation, job_id)
    return {"message": "Job queued for retry", "job_id": job_id}

@app.post("/api/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a pending job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs[job_id]
    if job["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending jobs can be cancelled")

    update_job(job_id, status="cancelled", message="Cancelled by user")
    return {"message": "Job cancelled", "job_id": job_id}

@app.delete("/api/jobs")
async def clear_completed_jobs():
    """Clear all completed/failed/cancelled jobs."""
    to_remove = [jid for jid, j in jobs.items() if j["status"] in ("completed", "failed", "cancelled")]
    for jid in to_remove:
        del jobs[jid]
    save_jobs()
    broadcast_sse("jobs_cleared", {"count": len(to_remove)})
    return {"message": f"Cleared {len(to_remove)} jobs"}

# ============== Videos ==============

@app.get("/api/videos")
async def list_videos():
    videos = []
    for folder in VIDEOS_DIR.iterdir():
        if folder.is_dir():
            video_file = folder / "final_video.mp4"
            metadata_file = folder / "seo_metadata.json"

            if video_file.exists():
                video_info = {
                    "id": folder.name, "name": folder.name,
                    "url": f"/videos/{folder.name}/final_video.mp4",
                    "size_mb": round(video_file.stat().st_size / (1024 * 1024), 1),
                    "created": datetime.fromtimestamp(video_file.stat().st_mtime).isoformat()
                }

                # Extract domain from folder name (format: DomainName_Xmin_timestamp)
                parts = folder.name.split("_")
                if len(parts) >= 2:
                    video_info["domain"] = parts[0]

                if metadata_file.exists():
                    with open(metadata_file) as f:
                        seo = json.load(f)
                        video_info["title"] = seo.get("title", folder.name)
                        video_info["description"] = seo.get("description", "")
                        video_info["hashtags"] = seo.get("hashtags", [])

                yt_info_file = folder / "youtube_info.json"
                if yt_info_file.exists():
                    with open(yt_info_file) as f:
                        video_info["youtube_info"] = json.load(f)

                videos.append(video_info)

    return {"videos": sorted(videos, key=lambda x: x["created"], reverse=True)}

@app.get("/api/videos/{video_id}/download")
async def download_video(video_id: str):
    video_path = VIDEOS_DIR / video_id / "final_video.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path, media_type="video/mp4", filename=f"{video_id}.mp4")

@app.delete("/api/videos/{video_id}")
async def delete_video(video_id: str):
    video_dir = VIDEOS_DIR / video_id
    if not video_dir.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    shutil.rmtree(video_dir)
    to_remove = [jid for jid, j in jobs.items() if j.get("video_url", "").find(video_id) != -1]
    for jid in to_remove:
        del jobs[jid]
    save_jobs()
    return {"message": f"Deleted {video_id}"}

# ============== YouTube Publishing ==============

@app.get("/api/youtube/status")
async def youtube_status():
    token_path = Path("youtube_token.pickle")
    return {"connected": token_path.exists()}

@app.get("/api/videos/{video_id}/metadata")
async def get_video_metadata(video_id: str):
    meta_path = VIDEOS_DIR / video_id / "seo_metadata.json"
    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="Metadata not found")
    with open(meta_path) as f:
        return json.load(f)

@app.api_route("/api/videos/{video_id}/thumbnail", methods=["GET", "POST"])
async def generate_thumbnail_preview(video_id: str):
    video_dir = VIDEOS_DIR / video_id
    if not video_dir.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    images_dir = video_dir / "images"
    meta_path = video_dir / "seo_metadata.json"
    title = video_id
    if meta_path.exists():
        with open(meta_path) as f:
            title = json.load(f).get("title", video_id)
    thumb_path = video_dir / "thumbnail.jpg"
    generate_thumbnail(title, str(images_dir), str(thumb_path))
    return FileResponse(thumb_path, media_type="image/jpeg")

@app.post("/api/publish/{job_id}")
async def publish_to_youtube(job_id: str, request: PublishRequest):
    video_dir = VIDEOS_DIR / job_id
    video_path = video_dir / "final_video.mp4"

    if not video_path.exists():
        if job_id in jobs and jobs[job_id].get("video_path"):
            video_path = Path(jobs[job_id]["video_path"])
            video_dir = video_path.parent
        else:
            raise HTTPException(status_code=404, detail="Video not found")

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    token_path = Path("youtube_token.pickle")
    if not token_path.exists():
        raise HTTPException(status_code=400, detail="YouTube not connected. Run youtube_auth.py first.")

    # Auto-fill title/description/tags from seo_metadata if not provided
    seo_path = video_dir / "seo_metadata.json"
    seo = {}
    if seo_path.exists():
        with open(seo_path) as f:
            seo = json.load(f)

    title = request.title or seo.get("title", job_id)
    description = request.description or seo.get("description", "")
    tags = request.tags or seo.get("tags", [])

    try:
        images_dir = video_dir / "images"
        thumb_path = video_dir / "thumbnail.jpg"
        thumb = None
        if images_dir.exists():
            generate_thumbnail(title, str(images_dir), str(thumb_path))
            thumb = str(thumb_path)

        result = yt_upload_video(
            video_path=str(video_path), title=title,
            description=description, tags=tags,
            privacy=request.privacy if request.privacy == 'private' else 'public',
            thumbnail_path=thumb, schedule=True,
        )

        yt_info = {
            "video_id": result["video_id"], "url": result["url"],
            "published_at": datetime.now().isoformat(),
            "scheduled_at": result.get("scheduled_at"),
            "title": title, "privacy": request.privacy,
        }
        with open(video_dir / "youtube_info.json", "w") as f:
            json.dump(yt_info, f, indent=2)

        if job_id in jobs:
            jobs[job_id]["youtube_info"] = yt_info
            save_jobs()

        return {
            "video_id": result["video_id"], "youtube_url": result["url"],
            "scheduled_at": result.get("scheduled_at"),
            "status": "scheduled" if result.get("scheduled_at") else "published",
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/publish-bulk")
async def bulk_publish(request: BulkPublishRequest, background_tasks: BackgroundTasks):
    """Publish multiple videos to YouTube at once."""
    token_path = Path("youtube_token.pickle")
    if not token_path.exists():
        raise HTTPException(status_code=400, detail="YouTube not connected.")

    results = []
    errors = []

    for video_id in request.video_ids:
        video_dir = VIDEOS_DIR / video_id
        video_path = video_dir / "final_video.mp4"
        meta_path = video_dir / "seo_metadata.json"

        if not video_path.exists():
            errors.append({"video_id": video_id, "error": "Video not found"})
            continue

        title = video_id
        description = ""
        tags = []
        if meta_path.exists():
            with open(meta_path) as f:
                seo = json.load(f)
                title = seo.get("title", video_id)
                description = seo.get("description", "")
                tags = [h.replace("#", "") for h in seo.get("hashtags", [])]

        try:
            images_dir = video_dir / "images"
            thumb_path = video_dir / "thumbnail.jpg"
            thumb = None
            if images_dir.exists():
                generate_thumbnail(title, str(images_dir), str(thumb_path))
                thumb = str(thumb_path)

            result = yt_upload_video(
                video_path=str(video_path), title=title,
                description=description, tags=tags,
                privacy=request.privacy, thumbnail_path=thumb, schedule=True,
            )

            yt_info = {
                "video_id": result["video_id"], "url": result["url"],
                "published_at": datetime.now().isoformat(),
                "scheduled_at": result.get("scheduled_at"),
                "title": title, "privacy": request.privacy,
            }
            with open(video_dir / "youtube_info.json", "w") as f:
                json.dump(yt_info, f, indent=2)

            results.append({"video_id": video_id, "youtube_url": result["url"]})
        except Exception as e:
            errors.append({"video_id": video_id, "error": str(e)})

    return {"published": results, "errors": errors, "total": len(results), "failed": len(errors)}

# ============== Leonardo AI Credits ==============

@app.get("/api/credits")
async def get_leonardo_credits():
    api_key = os.getenv("LEONARDO_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="LEONARDO_API_KEY not set")
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://cloud.leonardo.ai/api/rest/v1/me",
            headers={"authorization": f"Bearer {api_key}", "accept": "application/json"},
            timeout=10,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch credits")
        data = resp.json()
        user_info = data.get("user_details", [{}])[0] if data.get("user_details") else {}
        return {
            "api_credits": user_info.get("apiConcurrencySlots", 0),
            "subscription_tokens": user_info.get("subscriptionTokens", 0),
            "api_plan_token_renewal_date": user_info.get("apiPlanTokenRenewalDate"),
            "raw": user_info,
        }

# ============== Automation State ==============

@app.get("/api/automation-state")
async def get_automation_state():
    """Expose current automation rotation state."""
    state = load_automation_state()
    domain_names = list(DOMAIN_REGISTRY.keys())
    current_domain_idx = state.get("domain_index", 0) % len(domain_names) if domain_names else 0
    return {
        **state,
        "current_domain": domain_names[current_domain_idx] if domain_names else None,
        "total_domains": len(domain_names),
        "domain_names": domain_names,
    }

# ============== Batch Generation ==============

class BatchRequest(BaseModel):
    count: int = 1

@app.post("/api/generate-batch")
async def generate_batch(request: BatchRequest, background_tasks: BackgroundTasks):
    if request.count < 1 or request.count > 50:
        raise HTTPException(status_code=400, detail="Count must be 1-50")

    state = load_automation_state()
    domain_names = list(DOMAIN_REGISTRY.keys())
    library = load_music_library()
    # Duration options (seconds). Comment/uncomment to enable/disable.
    # To re-enable 7 and 10 min, simply uncomment them below:
    base_durations = [
        180,   # 3 min
        300,   # 5 min
        # 420, # 7 min  — disabled (uncomment to enable)
        # 600, # 10 min — disabled (uncomment to enable)
    ]

    job_ids = []
    for i in range(request.count):
        domain_name = domain_names[state["domain_index"] % len(domain_names)]
        domain = DOMAIN_REGISTRY[domain_name]
        base_dur = base_durations[state.get("duration_toggle", state.get("duration_index", 0)) % len(base_durations)]
        # Add random 5-45 seconds for natural variation
        dur = base_dur + random.randint(5, 45)
        if dur <= 225:  # base 180 + up to 45s variation
            music_pool = library.get("short", [])
        else:
            music_pool = library.get("long", [])
        music_track = music_pool[state["music_index"] % len(music_pool)] if music_pool else None
        music_path = str(MUSIC_DIR / music_track["filename"]) if music_track else None
        music_id = music_track["id"] if music_track else None
        music_name = music_track["name"] if music_track else None

        custom_desc = generate_auto_prompt(domain, dur)

        job_id = str(uuid.uuid4())[:8]
        jobs[job_id] = {
            "job_id": job_id, "status": "pending", "progress": 0,
            "message": "Queued (batch)", "domain": domain_name, "duration": dur,
            "custom_description": custom_desc, "music_id": music_id,
            "music_path": music_path, "music_name": music_name,
            "created_at": datetime.now().isoformat(), "completed_at": None,
            "video_path": None, "video_url": None, "scenes": None,
            "seo_metadata": None, "error": None, "batch": True,
        }
        job_ids.append(job_id)
        broadcast_sse("job_created", jobs[job_id])

        state["domain_index"] = state.get("domain_index", 0) + 1
        # Normalize key name
        dt_key = "duration_toggle" if "duration_toggle" in state else "duration_index"
        state[dt_key] = state.get(dt_key, 0) + 1
        state["music_index"] = state.get("music_index", 0) + 1
        state["total_generated"] = state.get("total_generated", 0) + 1

    save_automation_state(state)
    save_jobs()

    background_tasks.add_task(run_batch_jobs, job_ids)
    return {"job_ids": job_ids, "count": len(job_ids), "message": f"Queued {len(job_ids)} videos"}

async def run_batch_jobs(job_ids: list):
    for job_id in job_ids:
        if jobs.get(job_id, {}).get("status") == "cancelled":
            continue
        await run_generation(job_id)

# ============== Health Check ==============

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_keys": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "leonardo": bool(os.getenv("LEONARDO_API_KEY"))
        },
        "jobs": {
            "total": len(jobs),
            "running": sum(1 for j in jobs.values() if j["status"] == "running"),
            "pending": sum(1 for j in jobs.values() if j["status"] == "pending"),
        }
    }

# ============== Shorts Generation ==============

from core.shorts_generator import ShortsGenerator
from shorts.hooks import HOOK_LINES, EMOTIONAL_CLOSERS

SHORTS_JOBS_FILE = Path("shorts_jobs_store.json")
shorts_jobs: Dict[str, Dict[str, Any]] = {}
SHORTS_VIDEOS_DIR = Path("generated_shorts")
SHORTS_VIDEOS_DIR.mkdir(exist_ok=True)

app.mount("/shorts", StaticFiles(directory="generated_shorts"), name="shorts")

def load_shorts_jobs():
    global shorts_jobs
    if SHORTS_JOBS_FILE.exists():
        try:
            with open(SHORTS_JOBS_FILE) as f:
                shorts_jobs = json.load(f)
        except Exception:
            shorts_jobs = {}

def save_shorts_jobs():
    try:
        with open(SHORTS_JOBS_FILE, "w") as f:
            json.dump(shorts_jobs, f, indent=2, default=str)
    except Exception:
        pass

def update_shorts_job(job_id: str, **kwargs):
    if job_id in shorts_jobs:
        shorts_jobs[job_id].update(kwargs)
        save_shorts_jobs()
        event_data = json.dumps(shorts_jobs[job_id], default=str)
        for q in sse_subscribers:
            try:
                q.put_nowait({"event": "shorts_job_update", "data": event_data})
            except asyncio.QueueFull:
                pass

# Load shorts jobs on startup - hook into lifespan via post-init
load_shorts_jobs()

class ShortsRequest(BaseModel):
    domain: Optional[str] = None
    hook_category: Optional[str] = None
    duration: int = 45

class ShortsBatchRequest(BaseModel):
    count: int = 1

@app.post("/api/shorts/generate")
async def generate_short(request: ShortsRequest, background_tasks: BackgroundTasks):
    domain_name = request.domain
    if domain_name and domain_name not in DOMAIN_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid domain: {domain_name}")
    if not domain_name:
        domain_name = random.choice(list(DOMAIN_REGISTRY.keys()))
    if request.duration < 30 or request.duration > 60:
        raise HTTPException(status_code=400, detail="Duration must be 30-60 seconds")

    job_id = "s-" + str(uuid.uuid4())[:8]
    shorts_jobs[job_id] = {
        "job_id": job_id, "status": "pending", "progress": 0,
        "message": "Queued", "domain": domain_name,
        "duration": request.duration, "hook_category": request.hook_category,
        "created_at": datetime.now().isoformat(), "completed_at": None,
        "video_path": None, "video_url": None, "hook_text": None,
        "seo_metadata": None, "error": None,
    }
    save_shorts_jobs()
    broadcast_sse("shorts_job_created", shorts_jobs[job_id])
    background_tasks.add_task(run_shorts_generation, job_id)
    return {"job_id": job_id, "status": "pending", "message": "Short generation started"}

@app.post("/api/shorts/generate-batch")
async def generate_shorts_batch(request: ShortsBatchRequest, background_tasks: BackgroundTasks):
    if request.count < 1 or request.count > 20:
        raise HTTPException(status_code=400, detail="Count must be 1-20")
    domain_names = list(DOMAIN_REGISTRY.keys())
    categories = list(HOOK_LINES.keys())
    job_ids = []
    for i in range(request.count):
        domain_name = domain_names[i % len(domain_names)]
        cat = categories[i % len(categories)]
        dur = random.randint(35, 55)
        job_id = "s-" + str(uuid.uuid4())[:8]
        shorts_jobs[job_id] = {
            "job_id": job_id, "status": "pending", "progress": 0,
            "message": "Queued (batch)", "domain": domain_name,
            "duration": dur, "hook_category": cat,
            "created_at": datetime.now().isoformat(), "completed_at": None,
            "video_path": None, "video_url": None, "hook_text": None,
            "seo_metadata": None, "error": None,
        }
        job_ids.append(job_id)
        broadcast_sse("shorts_job_created", shorts_jobs[job_id])
    save_shorts_jobs()
    background_tasks.add_task(run_shorts_batch, job_ids)
    return {"job_ids": job_ids, "count": len(job_ids), "message": f"Queued {len(job_ids)} shorts"}

@app.get("/api/shorts/hooks")
async def list_hooks():
    return {
        "categories": {k: v for k, v in HOOK_LINES.items()},
        "emotional_closers": EMOTIONAL_CLOSERS,
        "total_hooks": sum(len(v) for v in HOOK_LINES.values()),
        "total_closers": len(EMOTIONAL_CLOSERS),
    }

@app.get("/api/shorts/jobs")
async def list_shorts_jobs():
    return {"jobs": list(shorts_jobs.values())}

@app.get("/api/shorts/videos")
async def list_shorts_videos():
    videos = []
    for folder in SHORTS_VIDEOS_DIR.iterdir():
        if folder.is_dir():
            vf = folder / "short_video.mp4"
            if vf.exists():
                info = {
                    "id": folder.name,
                    "url": f"/shorts/{folder.name}/short_video.mp4",
                    "size_mb": round(vf.stat().st_size / (1024 * 1024), 1),
                    "created": datetime.fromtimestamp(vf.stat().st_mtime).isoformat(),
                }
                meta = folder / "seo_metadata.json"
                if meta.exists():
                    with open(meta) as f:
                        seo = json.load(f)
                    info["title"] = seo.get("title", folder.name)
                    info["description"] = seo.get("description", "")
                sd = folder / "short_data.json"
                if sd.exists():
                    with open(sd) as f:
                        d = json.load(f)
                    info["hook_text"] = d.get("hook_text", "")
                    info["domain"] = folder.name.split("_")[0] if "_" in folder.name else ""
                videos.append(info)
    return {"videos": sorted(videos, key=lambda x: x["created"], reverse=True)}

@app.delete("/api/shorts/jobs/{job_id}")
async def delete_shorts_job(job_id: str):
    if job_id not in shorts_jobs:
        raise HTTPException(status_code=404, detail="Shorts job not found")
    del shorts_jobs[job_id]
    save_shorts_jobs()
    return {"message": "Shorts job deleted"}

async def run_shorts_generation(job_id: str):
    job = shorts_jobs.get(job_id)
    if not job or job.get("status") == "cancelled":
        return
    try:
        update_shorts_job(job_id, status="running", message="Initializing...")
        domain = DOMAIN_REGISTRY[job["domain"]]
        gen = ShortsGenerator()
        folder_name = f"{domain.name.replace(' ', '')}_{job['duration']}s_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_folder = SHORTS_VIDEOS_DIR / folder_name
        project_folder.mkdir(parents=True, exist_ok=True)

        def progress_cb(pct, msg):
            update_shorts_job(job_id, progress=pct, message=msg)

        loop = asyncio.get_event_loop()
        output_path, scene_data, seo = await loop.run_in_executor(
            None,
            lambda: gen.generate_short(
                domain=domain,
                hook_category=job.get("hook_category"),
                target_duration=job["duration"],
                project_folder=project_folder,
                progress_callback=progress_cb,
            ),
        )
        update_shorts_job(
            job_id, status="completed", progress=100,
            message="Short complete!", completed_at=datetime.now().isoformat(),
            video_path=str(output_path),
            video_url=f"/shorts/{folder_name}/short_video.mp4",
            hook_text=scene_data.get("hook_text"),
            seo_metadata=seo,
        )
    except Exception as e:
        update_shorts_job(job_id, status="failed", error=str(e), message=f"Error: {e}")

async def run_shorts_batch(job_ids: list):
    for jid in job_ids:
        if shorts_jobs.get(jid, {}).get("status") == "cancelled":
            continue
        await run_shorts_generation(jid)


# ============== Ideas Bank ==============

@app.get("/api/ideas/stats")
async def get_idea_stats():
    """Get idea bank stats."""
    return idea_bank.get_stats()

@app.get("/api/ideas")
async def list_ideas(status: str = None, limit: int = 20):
    """List ideas, optionally filtered by status."""
    ideas = idea_bank.get_all_ideas(status=status)
    return {"ideas": ideas[:limit], "total": len(ideas)}

@app.post("/api/ideas/generate")
async def generate_ideas_endpoint(background_tasks: BackgroundTasks):
    """Generate 100 new unique ideas in background."""
    progress = idea_bank.get_generation_progress()
    if progress.get("active"):
        return {"message": "Generation already in progress", "progress": progress}

    def _gen_sync():
        import asyncio
        try:
            print("[IDEAS] Starting idea generation...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(idea_bank.generate_ideas(100))
            print(f"[IDEAS] Generation complete: {result} ideas generated")
            loop.close()
        except Exception as e:
            import traceback
            print(f"[IDEAS] Generation error: {e}")
            traceback.print_exc()

    background_tasks.add_task(_gen_sync)
    return {"message": "Generating 100 ideas in background", "status": "started"}

@app.get("/api/ideas/generating")
async def ideas_generation_status():
    """Check idea generation progress."""
    return idea_bank.get_generation_progress()

# ============== Calendar ==============

@app.get("/api/calendar/{year}/{month}")
async def get_calendar(year: int, month: int):
    """Get content calendar for a month."""
    import calendar as cal_mod
    entries = content_calendar.get_month(year, month)
    # Build day slots
    _, days_in_month = cal_mod.monthrange(year, month)
    days = {}
    for day in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        days[date_str] = [e for e in entries if e.get("date") == date_str]
    return {"year": year, "month": month, "days": days, "entries": entries}

@app.get("/api/calendar/stats")
async def get_calendar_stats():
    """Publishing stats."""
    return content_calendar.get_stats()

# ============== Auto Publisher ==============

@app.get("/api/autopublish/status")
async def autopublish_status():
    """Auto-publisher status."""
    return auto_publisher.get_status()

@app.post("/api/autopublish/toggle")
async def toggle_autopublish():
    """Enable/disable auto-publishing."""
    enabled = auto_publisher.toggle()
    return {"enabled": enabled}

@app.get("/api/autopublish/schedule")
async def get_publish_schedule():
    """Get upcoming 14-day publish schedule."""
    return {"slots": auto_publisher.get_next_publish_slots(28)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3011)
