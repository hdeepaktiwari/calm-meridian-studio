"""Retry failed video jobs — reuses existing images, just does assembly + music."""
import sys
sys.path.insert(0, '.')

from pathlib import Path
from core.video_generator import VideoGenerator
from dotenv import load_dotenv
load_dotenv()

gen = VideoGenerator()
base = Path("generated_videos")

# Failed jobs with their params
failed = [
    ("1770550788_Modern_Luxury_Mansions_300s", "Modern Luxury Mansions", 300, "music/winter piano_10_30.mp3"),
    ("1770551123_Lush_Agricultural_Farmhouses_180s", "Lush Agricultural Farmhouses", 180, "music/suspense_3_24.mp3"),
]

for folder_name, domain_name, duration, music_path in failed:
    folder = base / folder_name
    if not folder.exists():
        print(f"❌ Folder not found: {folder}")
        continue
    
    images_dir = folder / "images"
    if not images_dir.exists() or len(list(images_dir.glob("*.jpg"))) == 0:
        print(f"❌ No images in: {folder}")
        continue
    
    print(f"\n🎬 Retrying: {folder_name}")
    print(f"   Domain: {domain_name}, Duration: {duration}s, Music: {music_path}")
    print(f"   Images: {len(list(images_dir.glob('*.jpg')))} found")
    
    try:
        from domains import DOMAIN_REGISTRY
        domain = DOMAIN_REGISTRY[domain_name]
        
        def progress(pct, msg=""):
            print(f"   [{pct}%] {msg}")
        
        # The generate_video method handles everything including reusing existing images
        gen.generate_video(
            domain=domain,
            duration=duration,
            custom_description="",
            audio_path=music_path,
            project_folder=folder,
            use_domain_weights=True,
            include_signature=True,
            optimize_lighting=True,
            progress_callback=progress,
        )
        print(f"   ✅ Done! {folder / 'final_video.mp4'}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
