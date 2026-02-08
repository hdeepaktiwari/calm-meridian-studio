"""
File Manager - Handles organized file structure for video projects
"""
import os
import time
import json
from pathlib import Path

class FileManager:
    def __init__(self, base_dir="generated_videos"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def create_project_folder(self, domain_name, duration):
        """Create organized project folder"""
        timestamp = int(time.time())
        clean_name = "".join(c for c in domain_name if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_name = clean_name.replace(' ', '_')
        
        folder_name = f"{timestamp}_{clean_name}_{duration}s"
        project_folder = self.base_dir / folder_name
        
        # Create subdirectories
        project_folder.mkdir(parents=True, exist_ok=True)
        (project_folder / "images").mkdir(exist_ok=True)
        (project_folder / "scenes").mkdir(exist_ok=True)
        
        return project_folder
    
    def save_audio(self, audio_file, project_folder):
        """Save uploaded audio file"""
        audio_path = project_folder / audio_file.name
        with open(audio_path, 'wb') as f:
            f.write(audio_file.getbuffer())
        return audio_path
    
    def save_metadata(self, project_folder, domain, duration, scenes, audio_name):
        """Save comprehensive project metadata"""
        
        # Create README
        readme_path = project_folder / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"""
╔══════════════════════════════════════════════════════════╗
║         CINEMATIC VIDEO STUDIO PROJECT                   ║
╚══════════════════════════════════════════════════════════╝

📁 PROJECT: {project_folder.name}
📅 GENERATED: {time.strftime('%Y-%m-%d %H:%M:%S')}

🎬 DOMAIN
{domain.icon} {domain.name}
{domain.description}

⏱️ DURATION
{duration} seconds ({duration // 60}:{duration % 60:02d})

🎨 STYLE
Color Palette: {', '.join(domain.color_palette)}
Mood: {', '.join(domain.mood_keywords)}
Lighting: {', '.join(domain.lighting_conditions)}

📊 VIDEO DETAILS
- Resolution: 1920x1080 (Full HD)
- FPS: 30
- Bitrate: 10000k (Ultra High Quality)
- Total Scenes: {len(scenes)}
- Format: MP4 (H.264 + AAC)

📂 FOLDER STRUCTURE
├── final_video.mp4          ← Your completed video
├── scene_plan.json          ← AI-generated scene plan
├── README.txt               ← This file
├── images/                  ← All generated images
│   ├── scene_01_*.jpg
│   ├── scene_02_*.jpg
│   └── ...
├── scenes/                  ← Individual scene information
│   ├── scene_01_*_info.json
│   ├── scene_02_*_info.json
│   └── ...
└── {audio_name if audio_name else '(no background music)'}

🎲 RANDOMIZATION
✓ Scene order shuffled for variation
✓ Camera movements weighted by domain
✓ Unique every generation

🎬 SCENE BREAKDOWN
""")
            
            for scene in scenes:
                f.write(f"\n{scene['scene_number']}. {scene['location']}")
                f.write(f"\n   Camera: {scene['camera_movement']}")
                f.write(f"\n   Lighting: {scene['lighting']}")
                f.write(f"\n   Mood: {scene.get('mood', 'cinematic')}")
                f.write(f"\n   Elements: {', '.join(scene['key_elements'])}")
                f.write(f"\n   {scene['description'][:100]}...")
                f.write("\n")
            
            f.write(f"""
╔══════════════════════════════════════════════════════════╗
║         POWERED BY CINEMATIC VIDEO STUDIO                ║
╚══════════════════════════════════════════════════════════╝

AI-Generated with:
• OpenAI GPT-4o-mini (Scene Planning)
• Leonardo AI (Image Generation)
• MoviePy (Video Assembly)
""")
        
        # Save project metadata JSON
        metadata_path = project_folder / "project_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                "project_name": project_folder.name,
                "timestamp": int(time.time()),
                "domain": {
                    "name": domain.name,
                    "icon": domain.icon,
                    "description": domain.description
                },
                "duration": duration,
                "total_scenes": len(scenes),
                "audio_file": audio_name,
                "settings": {
                    "resolution": "1920x1080",
                    "fps": 30,
                    "bitrate": "10000k",
                    "format": "MP4"
                }
            }, f, indent=2)
        
        return readme_path