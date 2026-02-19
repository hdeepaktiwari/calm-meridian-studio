"""
Shorts Video Generator for Calm Meridian Studio.
Generates vertical 1080×1920 YouTube Shorts (30-60 seconds).
"""
import os
import json
import time
import random
import requests
import numpy as np
from openai import OpenAI
from moviepy import AudioFileClip, concatenate_videoclips, VideoClip, CompositeAudioClip
from moviepy.audio.fx import AudioFadeOut, AudioFadeIn
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from shorts.hooks import get_hook_for_domain, HOOK_LINES, EMOTIONAL_CLOSERS
from shorts.ambient_sounds import get_ambient_for_domain, get_fallback_music


class ShortsGenerator:
    """Generates vertical YouTube Shorts videos."""

    WIDTH = 1080
    HEIGHT = 1920
    FPS = 30

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.leonardo_api_key = os.getenv("LEONARDO_API_KEY")
        self.leonardo_base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.leonardo_headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.leonardo_api_key}",
            "content-type": "application/json",
        }
        self.base_style = (
            "Ultra detailed 8k cinematic photography, photorealistic, "
            "dramatic lighting, atmospheric depth, volumetric rays, "
            "museum quality composition, professional color grading, vertical framing"
        )

    # ------------------------------------------------------------------ #
    # Scene planning
    # ------------------------------------------------------------------ #
    def plan_scenes(self, domain, num_scenes: int = 4):
        """Use GPT-4o-mini to plan vertical scenes for a Short."""
        locations = random.sample(domain.locations, min(num_scenes, len(domain.locations)))
        if len(locations) < num_scenes:
            locations.extend(random.choices(domain.locations, k=num_scenes - len(locations)))

        prompt = f"""You are a cinematographer creating a {num_scenes}-scene vertical SHORT video for: {domain.name}

Description: {domain.description}

Create {num_scenes} visually stunning scenes. These are for a VERTICAL 9:16 video (phone format).

Locations available: {', '.join(domain.locations)}
Signature elements: {', '.join(domain.signature_elements[:8])}
Color palette: {', '.join(domain.color_palette)}
Mood: {', '.join(domain.mood_keywords)}

Return ONLY valid JSON:
{{
  "scenes": [
    {{
      "scene_number": 1,
      "location": "Specific location",
      "description": "Detailed vertical-composition visual description emphasizing height and depth",
      "lighting": "lighting type",
      "key_elements": ["element1", "element2"],
      "mood": "mood keyword"
    }}
  ]
}}"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are an expert {domain.name} cinematographer specialising in vertical/portrait compositions. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.9,
            max_tokens=2000,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()

        scenes = json.loads(content)["scenes"]
        random.shuffle(scenes)
        for i, s in enumerate(scenes, 1):
            s["scene_number"] = i
            s["camera_movement"] = random.choices(
                list(domain.camera_weights.keys()),
                weights=list(domain.camera_weights.values()),
            )[0]
        return scenes

    # ------------------------------------------------------------------ #
    # Image generation (Leonardo AI – vertical)
    # ------------------------------------------------------------------ #
    def _create_prompt(self, scene, domain):
        desc = scene["description"]
        lighting = scene["lighting"]
        elements = ", ".join(scene["key_elements"])
        mood = scene.get("mood", domain.mood_keywords[0])
        return (
            f"{desc}. {lighting} lighting. Mood: {mood}. Key elements: {elements}. "
            f"{domain.style_prompt}. Color palette: {', '.join(domain.color_palette)}. "
            f"{self.base_style}. Vertical portrait composition, tall framing."
        )

    def generate_image(self, prompt: str, name: str, images_dir: Path):
        path = images_dir / f"{name}.jpg"
        if path.exists():
            return str(path)

        data = {
            "alchemy": False,
            "height": 1920,
            "width": 1080,
            "modelId": "7b592283-e8a7-4c5a-9ba6-d18c31f258b9",
            "contrast": 3.5,
            "num_images": 1,
            "styleUUID": "111dc692-d470-4eec-b791-3475abac4c46",
            "prompt": prompt,
            "ultra": False,
        }
        resp = requests.post(f"{self.leonardo_base_url}/generations", headers=self.leonardo_headers, json=data)
        resp.raise_for_status()
        gen_id = resp.json()["sdGenerationJob"]["generationId"]

        for _ in range(60):
            time.sleep(3)
            sr = requests.get(f"{self.leonardo_base_url}/generations/{gen_id}", headers=self.leonardo_headers)
            sr.raise_for_status()
            sd = sr.json()["generations_by_pk"]
            if sd["status"] == "COMPLETE":
                url = sd["generated_images"][0]["url"]
                img_resp = requests.get(url)
                img_resp.raise_for_status()
                with open(path, "wb") as f:
                    f.write(img_resp.content)
                return str(path)
            elif sd["status"] == "FAILED":
                raise Exception("Leonardo image generation failed")
        raise Exception("Leonardo image generation timeout")

    # ------------------------------------------------------------------ #
    # Camera effects (vertical-adapted, slower)
    # ------------------------------------------------------------------ #
    def apply_camera_effect(self, image_path: str, movement: str, duration: float):
        img = Image.open(image_path)
        w, h = img.size  # Should be 1080×1920

        # Slower factor for shorts (contemplative)
        factor = 0.08

        if movement == "zoom_in":
            def make_frame(t):
                p = t / duration
                z = 1.0 + factor * p
                nw, nh = int(w * z), int(h * z)
                zoomed = img.resize((nw, nh), Image.LANCZOS)
                l, tp = (nw - w) // 2, (nh - h) // 2
                return np.array(zoomed.crop((l, tp, l + w, tp + h)))
        elif movement == "zoom_out":
            def make_frame(t):
                p = t / duration
                z = 1.0 + factor - factor * p
                nw, nh = int(w * z), int(h * z)
                zoomed = img.resize((nw, nh), Image.LANCZOS)
                l, tp = (nw - w) // 2, (nh - h) // 2
                return np.array(zoomed.crop((l, tp, l + w, tp + h)))
        elif movement == "pan_right":
            wide_w = int(w * (1 + factor * 2))
            wide_img = img.resize((wide_w, h), Image.LANCZOS)
            def make_frame(t):
                p = t / duration
                off = int((wide_w - w) * p)
                return np.array(wide_img.crop((off, 0, off + w, h)))
        elif movement == "pan_left":
            wide_w = int(w * (1 + factor * 2))
            wide_img = img.resize((wide_w, h), Image.LANCZOS)
            def make_frame(t):
                p = t / duration
                off = int((wide_w - w) * (1 - p))
                return np.array(wide_img.crop((off, 0, off + w, h)))
        elif movement == "tilt_up":
            tall_h = int(h * (1 + factor * 2))
            tall_img = img.resize((w, tall_h), Image.LANCZOS)
            def make_frame(t):
                p = t / duration
                off = int((tall_h - h) * (1 - p))
                return np.array(tall_img.crop((0, off, w, off + h)))
        else:
            arr = np.array(img)
            def make_frame(t):
                return arr

        return VideoClip(make_frame, duration=duration)

    # ------------------------------------------------------------------ #
    # Text frame rendering (PIL)
    # ------------------------------------------------------------------ #
    def _get_font(self, size: int):
        """Try to load a nice font, fall back to default."""
        for name in [
            "/System/Library/Fonts/Palatino.ttc",
            "/System/Library/Fonts/Supplemental/Palatino.ttc",
            "/System/Library/Fonts/Avenir.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]:
            if os.path.exists(name):
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def _wrap_text(self, text: str, font, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
        words = text.split()
        lines, current = [], ""
        for word in words:
            test = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [text]

    def create_hook_frames(self, hook_text: str, duration: float = 3.0) -> list[np.ndarray]:
        """Create hook frames: fade-in text on dark bg."""
        font = self._get_font(52)
        total_frames = int(duration * self.FPS)
        fade_in_frames = int(0.6 * self.FPS)  # 0.6s fade in
        fade_out_frames = int(0.4 * self.FPS)  # 0.4s fade out

        # Pre-render text image
        base = Image.new("RGB", (self.WIDTH, self.HEIGHT), (10, 10, 15))
        draw = ImageDraw.Draw(base)
        lines = self._wrap_text(hook_text, font, self.WIDTH - 160, draw)
        line_height = 70
        total_text_h = len(lines) * line_height
        y_start = (self.HEIGHT - total_text_h) // 2

        # Create text layer (RGBA)
        text_layer = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        td = ImageDraw.Draw(text_layer)
        for i, line in enumerate(lines):
            bbox = td.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (self.WIDTH - tw) // 2
            td.text((x, y_start + i * line_height), line, fill=(255, 255, 255, 255), font=font)

        base_arr = np.array(base)
        text_arr = np.array(text_layer)

        frames = []
        for fi in range(total_frames):
            if fi < fade_in_frames:
                alpha = fi / fade_in_frames
            elif fi >= total_frames - fade_out_frames:
                alpha = (total_frames - fi) / fade_out_frames
            else:
                alpha = 1.0
            # Composite
            frame = base_arr.copy()
            mask = (text_arr[:, :, 3] / 255.0 * alpha)[:, :, np.newaxis]
            frame = (frame * (1 - mask) + text_arr[:, :, :3] * mask).astype(np.uint8)
            frames.append(frame)
        return frames

    def create_end_frame(self, image_path: str, closer_text: str, duration: float = 6.0) -> list[np.ndarray]:
        """Create end frame: image with dark overlay + branding text."""
        img = Image.open(image_path).resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)
        # Dark overlay
        overlay = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 140))
        img_rgba = img.convert("RGBA")
        composited = Image.alpha_composite(img_rgba, overlay).convert("RGB")

        draw = ImageDraw.Draw(composited)
        brand_font = self._get_font(44)
        closer_font = self._get_font(28)

        # "Calm Meridian" centered
        brand = "Calm Meridian"
        bbox = draw.textbbox((0, 0), brand, font=brand_font)
        bw = bbox[2] - bbox[0]
        draw.text(((self.WIDTH - bw) // 2, self.HEIGHT // 2 - 40), brand, fill=(255, 255, 255), font=brand_font)

        # Closer text
        lines = self._wrap_text(closer_text, closer_font, self.WIDTH - 120, draw)
        y = self.HEIGHT // 2 + 30
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=closer_font)
            lw = bbox[2] - bbox[0]
            draw.text(((self.WIDTH - lw) // 2, y), line, fill=(220, 220, 220), font=closer_font)
            y += 40

        arr = np.array(composited)
        total_frames = int(duration * self.FPS)
        fade_in = int(0.8 * self.FPS)

        frames = []
        # We need a base (the scene image without overlay) for fade-in effect
        base_arr = np.array(img.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS))
        for fi in range(total_frames):
            if fi < fade_in:
                alpha = fi / fade_in
                frame = (base_arr * (1 - alpha) + arr * alpha).astype(np.uint8)
            else:
                frame = arr
            frames.append(frame)
        return frames

    # ------------------------------------------------------------------ #
    # SEO metadata for Shorts
    # ------------------------------------------------------------------ #
    def generate_seo(self, domain, hook_text: str, scenes) -> dict:
        """Generate YouTube Shorts SEO metadata."""
        scene_locs = ", ".join(s["location"] for s in scenes[:3])
        try:
            resp = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You write viral YouTube Shorts titles and descriptions. Return only valid JSON."},
                    {"role": "user", "content": f"""Create SEO metadata for a YouTube Short.
Domain: {domain.name}
Hook line: "{hook_text}"
Scenes: {scene_locs}

Return JSON:
{{
  "title": "Short engaging title ending with | Calm Meridian #Shorts (max 80 chars)",
  "description": "2-3 lines + hashtags. No CTAs. Poetic.",
  "tags": ["#Shorts", "#Calm", ...]
}}"""},
                ],
                temperature=0.8,
                max_tokens=500,
            )
            content = resp.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            seo = json.loads(content)
        except Exception:
            seo = {
                "title": f"{hook_text[:50]} | Calm Meridian #Shorts",
                "description": f"A moment of peace. {domain.name} in vertical cinema.\n\n#Shorts #Calm #Peace #Meditation",
                "tags": ["#Shorts", "#Calm", "#Peace", "#Meditation", "#Relaxation", "#ASMR", "#MentalHealth"],
            }
        # Ensure #Shorts in title
        if "#Shorts" not in seo.get("title", ""):
            seo["title"] = seo.get("title", "") + " #Shorts"
        # Add standard tags
        for tag in ["#Shorts", "#Calm", "#Peace", "#Meditation", "#Relaxation", "#ASMR", "#MentalHealth"]:
            if tag not in seo.get("tags", []):
                seo["tags"].append(tag)
        return seo

    # ------------------------------------------------------------------ #
    # Main generation pipeline
    # ------------------------------------------------------------------ #
    def generate_short(
        self,
        domain,
        hook_category: str = None,
        target_duration: int = 45,
        project_folder: Path = None,
        progress_callback=None,
    ) -> tuple[Path, dict, dict]:
        """
        Generate a complete YouTube Short.
        Returns (output_path, scene_data, seo_metadata).
        """
        if progress_callback is None:
            progress_callback = lambda p, m: None

        target_duration = max(30, min(60, target_duration))

        images_dir = project_folder / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        # 1. Pick hook & closer
        progress_callback(5, "✍️ Selecting hook...")
        hook_text, closer_text = get_hook_for_domain(domain.name, hook_category)

        # 2. Plan scenes
        hook_dur = 3.0
        end_dur = 6.0
        experience_dur = target_duration - hook_dur - end_dur
        num_scenes = max(3, min(4, int(experience_dur / 12)))
        scene_dur = experience_dur / num_scenes

        progress_callback(10, "🧠 Planning scenes...")
        scenes = self.plan_scenes(domain, num_scenes)

        # 3. Generate images
        for i, scene in enumerate(scenes):
            scene_name = f"short_scene_{i+1:02d}"
            prompt = self._create_prompt(scene, domain)
            pct = 15 + int(50 * (i + 1) / len(scenes))
            progress_callback(pct, f"🎨 Image {i+1}/{len(scenes)}: {scene['location']}")
            scene["image_path"] = self.generate_image(prompt, scene_name, images_dir)
            scene["duration"] = scene_dur

        # 4. Build clips
        progress_callback(70, "🎬 Building hook frame...")
        hook_frames = self.create_hook_frames(hook_text, hook_dur)
        hook_clip = VideoClip(lambda t, _f=hook_frames: _f[min(int(t * self.FPS), len(_f) - 1)], duration=hook_dur)

        progress_callback(73, "🎬 Applying camera effects...")
        experience_clips = []
        for scene in scenes:
            clip = self.apply_camera_effect(scene["image_path"], scene["camera_movement"], scene["duration"])
            experience_clips.append(clip)

        progress_callback(80, "🎬 Building end frame...")
        end_frames = self.create_end_frame(scenes[-1]["image_path"], closer_text, end_dur)
        end_clip = VideoClip(lambda t, _f=end_frames: _f[min(int(t * self.FPS), len(_f) - 1)], duration=end_dur)

        # 5. Concatenate
        all_clips = [hook_clip] + experience_clips + [end_clip]
        final_video = concatenate_videoclips(all_clips, method="compose")

        # 6. Audio
        progress_callback(85, "🔊 Adding ambient audio...")
        audio_path = get_ambient_for_domain(domain.name) or get_fallback_music()
        if audio_path and Path(audio_path).exists():
            audio = AudioFileClip(audio_path)
            vid_dur = final_video.duration
            if audio.duration < vid_dur:
                from moviepy import concatenate_audioclips
                loops = int(vid_dur / audio.duration) + 1
                audio = concatenate_audioclips([audio] * loops).with_duration(vid_dur)
            else:
                audio = audio.with_duration(vid_dur)
            # Very low volume for ambient feel (0.15 = 15%)
            audio = audio.with_volume_scaled(0.15)
            audio = audio.with_effects([AudioFadeOut(min(2.0, vid_dur * 0.1))])
            final_video = final_video.with_audio(audio)

        # 7. Export
        output_path = project_folder / "short_video.mp4"
        progress_callback(90, "💾 Rendering short...")
        final_video.write_videofile(
            str(output_path),
            fps=self.FPS,
            codec="libx264",
            audio_codec="aac",
            bitrate="8000k",
            preset="slow",
            threads=4,
            logger=None,
        )

        # Cleanup
        for c in all_clips:
            try:
                c.close()
            except Exception:
                pass
        final_video.close()

        # 8. SEO
        progress_callback(95, "🔍 Generating SEO...")
        seo = self.generate_seo(domain, hook_text, scenes)
        seo_path = project_folder / "seo_metadata.json"
        with open(seo_path, "w") as f:
            json.dump(seo, f, indent=2)

        scene_data = {
            "hook_text": hook_text,
            "closer_text": closer_text,
            "hook_category": hook_category,
            "scenes": scenes,
            "duration": target_duration,
        }
        # Save scene data
        with open(project_folder / "short_data.json", "w") as f:
            json.dump(scene_data, f, indent=2, default=str)

        progress_callback(100, "✅ Short complete!")
        return output_path, scene_data, seo
