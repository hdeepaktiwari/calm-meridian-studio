"""
Cinematic Video Studio API
FastAPI backend for video generation
"""
import os
import uuid
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

# Job storage (in-memory for now)
jobs: Dict[str, Dict[str, Any]] = {}

# Create directories
VIDEOS_DIR = Path("generated_videos")
VIDEOS_DIR.mkdir(exist_ok=True)
MUSIC_DIR = Path("music")
MUSIC_LIBRARY_FILE = MUSIC_DIR / "music_library.json"

def _get_leonardo_credits() -> dict:
    """Fetch Leonardo AI credit balance."""
    try:
        import requests as _req
        key = os.getenv("LEONARDO_API_KEY")
        if not key:
            return {"error": "No API key"}
        r = _req.get("https://cloud.leonardo.ai/api/rest/v1/me",
                      headers={"authorization": f"Bearer {key}", "accept": "application/json"}, timeout=5)
        data = r.json().get("user_details", [{}])[0]
        return {
            "api_paid_tokens": data.get("apiPaidTokens", 0),
            "api_subscription_tokens": data.get("apiSubscriptionTokens", 0),
            "total": data.get("apiPaidTokens", 0) + data.get("apiSubscriptionTokens", 0),
            "renewal_date": data.get("apiPlanTokenRenewalDate"),
        }
    except Exception as e:
        return {"error": str(e)}


def load_music_library():
    """Load music library from JSON"""
    if MUSIC_LIBRARY_FILE.exists():
        with open(MUSIC_LIBRARY_FILE) as f:
            return json.load(f)
    return {"short": [], "long": []}

# Automation state
AUTOMATION_STATE_FILE = Path("automation_state.json")
DURATIONS_CYCLE = [180, 300]
DOMAIN_ORDER = list(DOMAIN_REGISTRY.keys())  # preserves insertion order

def load_automation_state():
    if AUTOMATION_STATE_FILE.exists():
        with open(AUTOMATION_STATE_FILE) as f:
            return json.load(f)
    return {"domain_index": 0, "music_index": 0, "duration_index": 0, "total_generated": 0}

def save_automation_state(state):
    with open(AUTOMATION_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🎬 Cinematic Video Studio API starting...")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="Cinematic Video Studio API",
    description="AI-powered cinematic video generation",
    version="2.0.0",
    lifespan=lifespan
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated videos
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
    title: str
    description: str
    tags: list[str] = []
    privacy: str = 'private'

class GenerateRequest(BaseModel):
    domain: str
    duration: int  # seconds: 180, 300, 420, 600
    custom_description: Optional[str] = ""
    music_id: Optional[str] = None  # Music track ID from library

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
    status: str  # pending, running, completed, failed
    progress: int  # 0-100
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

# ============== API Endpoints ==============

@app.get("/")
async def root():
    return {
        "name": "Cinematic Video Studio API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "domains": "/api/domains",
            "generate": "/api/generate",
            "jobs": "/api/jobs",
            "job_status": "/api/jobs/{job_id}"
        }
    }

@app.get("/api/domains", response_model=Dict[str, DomainInfo])
async def get_domains():
    """Get all available cinematic domains"""
    result = {}
    for name, domain in DOMAIN_REGISTRY.items():
        result[name] = DomainInfo(
            name=domain.name,
            icon=domain.icon,
            description=domain.description,
            locations=domain.locations[:5],  # First 5
            signature_elements=domain.signature_elements[:5],
            color_palette=domain.color_palette,
            mood_keywords=domain.mood_keywords
        )
    return result

@app.get("/api/domains/{domain_name}")
async def get_domain(domain_name: str):
    """Get details for a specific domain"""
    if domain_name not in DOMAIN_REGISTRY:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    domain = DOMAIN_REGISTRY[domain_name]
    return {
        "name": domain.name,
        "icon": domain.icon,
        "description": domain.description,
        "locations": domain.locations,
        "signature_elements": domain.signature_elements,
        "lighting_conditions": domain.lighting_conditions,
        "color_palette": domain.color_palette,
        "mood_keywords": domain.mood_keywords
    }

# ============== Music Endpoints ==============

@app.get("/api/music")
async def get_music_library():
    """Get available music tracks organized by duration category"""
    library = load_music_library()
    return {
        "short": library.get("short", []),  # For 3-min videos
        "long": library.get("long", []),    # For 5, 7, 10-min videos
        "total": len(library.get("short", [])) + len(library.get("long", []))
    }

@app.get("/api/music/for-duration/{duration}")
async def get_music_for_duration(duration: int):
    """Get recommended music tracks for a specific video duration"""
    library = load_music_library()
    
    # For 3-min (180s) videos, use short tracks
    # For longer videos (300s+), use long tracks
    if duration <= 180:
        tracks = library.get("short", [])
        category = "short"
    else:
        tracks = library.get("long", [])
        category = "long"
    
    return {
        "category": category,
        "video_duration": duration,
        "tracks": tracks
    }

@app.get("/api/music/{music_id}")
async def get_music_track(music_id: str):
    """Get details for a specific music track"""
    library = load_music_library()
    
    for track in library.get("short", []) + library.get("long", []):
        if track["id"] == music_id:
            # Add file path for playback
            track["url"] = f"/music/{track['filename']}"
            return track
    
    raise HTTPException(status_code=404, detail="Music track not found")

# Serve music files for preview
app.mount("/music", StaticFiles(directory="music"), name="music")

@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Start video generation job"""
    
    # Validate domain
    if request.domain not in DOMAIN_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Invalid domain: {request.domain}")
    
    # Validate duration (3, 5, 7, 10 minutes)
    valid_durations = [180, 300, 420, 600]
    if request.duration not in valid_durations:
        raise HTTPException(status_code=400, detail=f"Duration must be one of {valid_durations}")
    
    # Resolve music path if provided
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
    
    # Create job
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "message": "Queued for processing",
        "domain": request.domain,
        "duration": request.duration,
        "custom_description": request.custom_description,
        "music_id": request.music_id,
        "music_path": music_path,
        "music_name": music_name,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "video_path": None,
        "video_url": None,
        "scenes": None,
        "seo_metadata": None,
        "error": None
    }
    
    # Start background task
    background_tasks.add_task(run_generation, job_id)
    
    return {"job_id": job_id, "status": "pending", "message": "Video generation started"}

async def run_generation(job_id: str):
    """Background task for video generation"""
    job = jobs[job_id]
    
    try:
        job["status"] = "running"
        job["message"] = "Initializing..."
        
        domain = DOMAIN_REGISTRY[job["domain"]]
        duration = job["duration"]
        custom_description = job.get("custom_description", "")
        music_path = job.get("music_path")
        
        # Initialize
        file_manager = FileManager("generated_videos")
        video_gen = VideoGenerator()
        
        # Create project folder
        project_folder = file_manager.create_project_folder(domain.name, duration)
        
        def progress_callback(percent, message):
            job["progress"] = percent
            job["message"] = message
        
        # Run generation (this is blocking, but we're in a background task)
        loop = asyncio.get_event_loop()
        output_path, scenes, seo_metadata = await loop.run_in_executor(
            None,
            lambda: video_gen.generate_video(
                domain=domain,
                duration=duration,
                custom_description=custom_description,
                audio_path=music_path,
                project_folder=project_folder,
                use_domain_weights=True,
                include_signature=True,
                optimize_lighting=True,
                progress_callback=progress_callback
            )
        )
        
        # Save metadata
        file_manager.save_metadata(
            project_folder,
            domain,
            duration,
            scenes,
            None
        )
        
        # Update job
        job["status"] = "completed"
        job["progress"] = 100
        job["message"] = "Video generation complete!"
        job["completed_at"] = datetime.now().isoformat()
        job["video_path"] = str(output_path)
        job["video_url"] = f"/videos/{project_folder.name}/final_video.mp4"
        job["scenes"] = scenes
        job["seo_metadata"] = seo_metadata
        
    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)
        job["message"] = f"Error: {str(e)}"

@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""
    return {"jobs": list(jobs.values())}

@app.get("/api/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get status of a specific job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    del jobs[job_id]
    return {"message": "Job deleted"}


@app.delete("/api/videos/{video_id}")
async def delete_video(video_id: str):
    """Delete a video permanently from storage and job list."""
    import shutil
    video_dir = VIDEOS_DIR / video_id
    if not video_dir.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    shutil.rmtree(video_dir)
    # Also remove from in-memory jobs if present
    if video_id in jobs:
        del jobs[video_id]
    return {"message": f"Video '{video_id}' deleted permanently"}

@app.get("/api/videos")
async def list_videos():
    """List all generated videos"""
    videos = []
    for folder in VIDEOS_DIR.iterdir():
        if folder.is_dir():
            video_file = folder / "final_video.mp4"
            metadata_file = folder / "seo_metadata.json"
            
            if video_file.exists():
                video_info = {
                    "id": folder.name,
                    "name": folder.name,
                    "url": f"/videos/{folder.name}/final_video.mp4",
                    "size_mb": round(video_file.stat().st_size / (1024 * 1024), 1),
                    "created": datetime.fromtimestamp(video_file.stat().st_mtime).isoformat()
                }
                
                if metadata_file.exists():
                    with open(metadata_file) as f:
                        seo = json.load(f)
                        video_info["title"] = seo.get("title", folder.name)
                        video_info["description"] = seo.get("description", "")
                        video_info["hashtags"] = seo.get("hashtags", [])

                # Thumbnail: use thumbnail.jpg or fall back to first scene image
                thumb_file = folder / "thumbnail.jpg"
                if thumb_file.exists():
                    video_info["thumbnail"] = f"/videos/{folder.name}/thumbnail.jpg"
                else:
                    images_dir = folder / "images"
                    if images_dir.exists():
                        imgs = sorted(images_dir.glob("*.jpg"))
                        if imgs:
                            video_info["thumbnail"] = f"/videos/{folder.name}/images/{imgs[0].name}"

                yt_info_file = folder / "youtube_info.json"
                if yt_info_file.exists():
                    with open(yt_info_file) as f:
                        video_info["youtube_info"] = json.load(f)
                
                videos.append(video_info)
    
    return {"videos": sorted(videos, key=lambda x: x["created"], reverse=True)}

@app.get("/api/videos/{video_id}/download")
async def download_video(video_id: str):
    """Download a video file"""
    video_path = VIDEOS_DIR / video_id / "final_video.mp4"
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )

# ============== YouTube Publishing ==============

@app.get("/api/youtube/status")
async def youtube_status():
    """Check if YouTube token exists"""
    token_path = Path("youtube_token.pickle")
    return {"connected": token_path.exists()}

@app.get("/api/videos/{video_id}/metadata")
async def get_video_metadata(video_id: str):
    """Get SEO metadata for a video"""
    meta_path = VIDEOS_DIR / video_id / "seo_metadata.json"
    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="Metadata not found")
    with open(meta_path) as f:
        return json.load(f)

@app.api_route("/api/videos/{video_id}/thumbnail", methods=["GET", "POST"])
async def generate_thumbnail_preview(video_id: str):
    """Generate thumbnail preview without uploading"""
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
    """Publish a video to YouTube"""
    # Find video directory - check both job dict and generated_videos folders
    video_dir = VIDEOS_DIR / job_id
    video_path = video_dir / "final_video.mp4"

    if not video_path.exists():
        # Try to find from jobs dict
        if job_id in jobs and jobs[job_id].get("video_path"):
            video_path = Path(jobs[job_id]["video_path"])
            video_dir = video_path.parent
        else:
            raise HTTPException(status_code=404, detail="Video not found")

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    # Check YouTube token
    token_path = Path("youtube_token.pickle")
    if not token_path.exists():
        raise HTTPException(status_code=400, detail="YouTube not connected. Run youtube_auth.py first.")

    try:
        # Generate thumbnail
        images_dir = video_dir / "images"
        thumb_path = video_dir / "thumbnail.jpg"
        thumb = None
        if images_dir.exists():
            generate_thumbnail(request.title, str(images_dir), str(thumb_path))
            thumb = str(thumb_path)

        # Upload to YouTube (auto-schedules for 8:00 AM IST)
        result = yt_upload_video(
            video_path=str(video_path),
            title=request.title,
            description=request.description,
            tags=request.tags,
            privacy=request.privacy if request.privacy == 'private' else 'public',
            thumbnail_path=thumb,
            schedule=True,
        )

        # Save youtube_info.json
        yt_info = {
            "video_id": result["video_id"],
            "url": result["url"],
            "published_at": datetime.now().isoformat(),
            "scheduled_at": result.get("scheduled_at"),
            "title": request.title,
            "privacy": request.privacy,
        }
        with open(video_dir / "youtube_info.json", "w") as f:
            json.dump(yt_info, f, indent=2)

        # Update job dict if exists
        if job_id in jobs:
            jobs[job_id]["youtube_info"] = yt_info

        return {
            "video_id": result["video_id"],
            "youtube_url": result["url"],
            "scheduled_at": result.get("scheduled_at"),
            "status": "scheduled" if result.get("scheduled_at") else "published",
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# ============== Batch Generation ==============

class BatchRequest(BaseModel):
    count: int = 1

@app.post("/api/generate-batch")
async def generate_batch(request: BatchRequest, background_tasks: BackgroundTasks):
    """Generate N videos using circular automation state."""
    if request.count < 1 or request.count > 50:
        raise HTTPException(status_code=400, detail="Count must be 1-50")

    state = load_automation_state()
    library = load_music_library()
    queued = []

    for i in range(request.count):
        # Pick domain
        domain_name = DOMAIN_ORDER[state["domain_index"] % len(DOMAIN_ORDER)]
        domain = DOMAIN_REGISTRY[domain_name]

        # Pick duration
        duration = DURATIONS_CYCLE[state["duration_index"] % len(DURATIONS_CYCLE)]

        # Pick music
        if duration <= 180:
            short_tracks = library.get("short", [])
            track = short_tracks[state["music_index"] % len(short_tracks)] if short_tracks else None
        else:
            long_tracks = library.get("long", [])
            track = long_tracks[state["music_index"] % len(long_tracks)] if long_tracks else None

        music_id = track["id"] if track else None
        music_path = str(MUSIC_DIR / track["filename"]) if track else None
        music_name = track.get("name", music_id) if track else None

        # Generate unique prompt
        custom_description = generate_auto_prompt(domain, duration, state["total_generated"])

        # Create job
        job_id = str(uuid.uuid4())[:8]
        jobs[job_id] = {
            "job_id": job_id,
            "status": "pending",
            "progress": 0,
            "message": "Queued for processing",
            "domain": domain_name,
            "duration": duration,
            "custom_description": custom_description,
            "music_id": music_id,
            "music_path": music_path,
            "music_name": music_name,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "video_path": None,
            "video_url": None,
            "scenes": None,
            "seo_metadata": None,
            "error": None,
        }

        background_tasks.add_task(run_generation, job_id)
        queued.append({"job_id": job_id, "domain": domain_name, "duration": duration, "music": music_name})

        # Increment indices
        state["domain_index"] += 1
        state["duration_index"] += 1
        state["music_index"] += 1
        state["total_generated"] += 1

    save_automation_state(state)
    return {"queued": queued, "count": len(queued), "state": state}

@app.get("/api/automation/next")
async def get_next_preview():
    """Preview what the next video will be."""
    state = load_automation_state()
    library = load_music_library()

    domain_name = DOMAIN_ORDER[state["domain_index"] % len(DOMAIN_ORDER)]
    duration = DURATIONS_CYCLE[state["duration_index"] % len(DURATIONS_CYCLE)]

    if duration <= 180:
        short_tracks = library.get("short", [])
        track = short_tracks[state["music_index"] % len(short_tracks)] if short_tracks else None
    else:
        long_tracks = library.get("long", [])
        track = long_tracks[state["music_index"] % len(long_tracks)] if long_tracks else None

    return {
        "domain": domain_name,
        "domain_icon": DOMAIN_REGISTRY[domain_name].icon,
        "duration": duration,
        "duration_label": f"{duration // 60}min",
        "music": track.get("name") if track else "None",
        "music_id": track.get("id") if track else None,
        "state": state,
    }

# ============== Config Endpoints ==============

@app.get("/api/config")
async def get_config():
    """Get full configuration."""
    state = load_automation_state()
    library = load_music_library()
    return {
        "domain_order": DOMAIN_ORDER,
        "domains": {name: {"icon": d.icon, "name": d.name} for name, d in DOMAIN_REGISTRY.items()},
        "music": library,
        "duration_cycle": DURATIONS_CYCLE,
        "api_status": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "leonardo": bool(os.getenv("LEONARDO_API_KEY")),
            "youtube": Path("youtube_token.pickle").exists(),
        },
        "automation_state": state,
    }

@app.get("/api/leonardo-credits")
async def get_leonardo_credits():
    """Fetch Leonardo AI credit balance on demand."""
    return _get_leonardo_credits()


@app.post("/api/config")
async def update_config(body: dict):
    """Update configuration (automation state reset, etc)."""
    if "reset_state" in body and body["reset_state"]:
        save_automation_state({"domain_index": 0, "music_index": 0, "duration_index": 0, "total_generated": 0})
    elif "automation_state" in body:
        save_automation_state(body["automation_state"])
    return {"status": "ok", "automation_state": load_automation_state()}

# ============== Health Check ==============

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_keys": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "leonardo": bool(os.getenv("LEONARDO_API_KEY"))
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3011)
