"""
Core Video Generator
Handles AI scene planning, image generation, and video assembly
"""
import os
import json
import time
import random
import requests
from openai import OpenAI
from moviepy import AudioFileClip, concatenate_videoclips, VideoClip, concatenate_audioclips, CompositeAudioClip
import numpy as np
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class VideoGenerator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.leonardo_api_key = os.getenv('LEONARDO_API_KEY')
        self.leonardo_base_url = "https://cloud.leonardo.ai/api/rest/v1"
        self.leonardo_headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.leonardo_api_key}",
            "content-type": "application/json"
        }
        
        self.base_style = """Ultra detailed 8k cinematic photography, photorealistic, 
        dramatic lighting, atmospheric depth, volumetric rays, museum quality composition, 
        professional color grading, cinematic framing"""
    
    def generate_scene_plan(self, domain, duration, custom_description, include_signature, optimize_lighting):
        """Generate AI scene plan tailored to domain with custom user description"""
        num_scenes = duration // 10
        
        # Select locations and elements
        locations = random.sample(domain.locations, min(num_scenes, len(domain.locations)))
        if len(locations) < num_scenes:
            locations.extend(random.choices(domain.locations, k=num_scenes - len(locations)))
        
        # Build prompt with domain knowledge
        elements_str = ", ".join(domain.signature_elements[:10])
        lighting_str = ", ".join(domain.lighting_conditions)
        locations_str = "\n".join([f"- {loc}" for loc in domain.locations])
        
        # Add custom description if provided
        custom_instructions = ""
        if custom_description and custom_description.strip():
            custom_instructions = f"\n\nUSER REQUIREMENTS:\n{custom_description}\nEnsure the scenes align with these specific requirements while maintaining the domain style."
        
        prompt = f"""You are a cinematographer creating a {duration}-second video for: {domain.name}

Description: {domain.description}{custom_instructions}

Create {num_scenes} distinct cinematic scenes using these locations:
{locations_str}

REQUIREMENTS:
1. Each scene must feature specific elements from this domain
2. Maintain visual continuity in style, color, and mood
3. Use appropriate lighting: {lighting_str}
4. Include these signature elements: {elements_str}
5. Make each scene visually distinct but thematically connected

Color Palette: {', '.join(domain.color_palette)}
Mood: {', '.join(domain.mood_keywords)}

Return ONLY valid JSON:
{{
  "scenes": [
    {{
      "scene_number": 1,
      "location": "Specific location name",
      "description": "Detailed visual description with specific elements",
      "lighting": "lighting type from: {lighting_str}",
      "key_elements": ["element1", "element2", "element3"],
      "mood": "mood keyword"
    }}
  ]
}}"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are an expert {domain.name} cinematographer. Return only valid JSON with rich visual details."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        
        plan = json.loads(content)
        scenes = plan['scenes']
        
        # Randomize scene order
        random.shuffle(scenes)
        
        # Assign camera movements using domain weights
        for i, scene in enumerate(scenes, 1):
            scene['scene_number'] = i
            scene['camera_movement'] = random.choices(
                list(domain.camera_weights.keys()),
                weights=list(domain.camera_weights.values())
            )[0]
        
        return scenes
    
    def search_trending_keywords(self, domain_name, custom_description=""):
        """Get trending keywords for the domain - uses curated list + web search if available"""
        
        # Curated trending keywords for relaxation/ambient content (2026)
        base_trending = {
            "global": [
                "4k", "8k hdr", "no ads", "10 hours", "sleep music 2026",
                "asmr", "lofi beats", "ambient sounds", "white noise",
                "deep sleep", "stress relief", "anxiety relief", "healing frequencies",
                "432hz", "528hz", "binaural beats", "meditation music",
                "study music", "focus music", "concentration", "productivity",
                "nature sounds", "rain sounds", "ocean waves", "forest sounds",
                "relaxing piano", "relaxing guitar", "calm music", "peaceful",
                "zen", "mindfulness", "yoga music", "spa music"
            ],
            "beaches": ["ocean waves", "beach ambience", "tropical vibes", "sunset beach", "coastal relaxation"],
            "forests": ["forest ambience", "birds chirping", "woodland sounds", "nature walk", "forest bathing"],
            "mountains": ["mountain serenity", "alpine peace", "himalayan", "mountain meditation", "peak tranquility"],
            "space": ["cosmic ambient", "space sounds", "galaxy", "nebula", "interstellar", "astronaut sleep"],
            "temples": ["temple bells", "sacred sounds", "spiritual", "ancient temples", "monastery"],
            "japanese_gardens": ["zen garden", "japanese ambient", "koi pond", "bamboo forest", "sakura"],
            "palaces": ["royal ambience", "palace halls", "majestic", "regal", "grand architecture"],
            "underwater": ["underwater sounds", "deep ocean", "marine life", "aquatic", "submarine"],
            "rain": ["rain sounds", "thunderstorm", "rainy day", "cozy rain", "rain on window"],
            "winter": ["winter ambience", "snowfall", "cozy winter", "fireplace", "cabin vibes"]
        }
        
        # Get domain-specific keywords
        domain_key = domain_name.lower().replace(" ", "_")
        domain_keywords = base_trending.get(domain_key, [])
        
        # Combine global + domain-specific
        all_keywords = base_trending["global"][:15] + domain_keywords
        
        # Try web search if Brave API key available
        brave_api_key = os.getenv('BRAVE_API_KEY')
        if brave_api_key:
            try:
                query = f"{domain_name} relaxation video trending YouTube 2026"
                headers = {
                    "Accept": "application/json",
                    "X-Subscription-Token": brave_api_key
                }
                response = requests.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers=headers,
                    params={"q": query, "count": 5},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    for result in data.get("web", {}).get("results", []):
                        text = f"{result.get('title', '')} {result.get('description', '')}".lower()
                        # Extract additional trending terms
                        for term in ["viral", "trending", "popular", "best", "top"]:
                            if term in text:
                                # Extract context around the term
                                idx = text.find(term)
                                context = text[max(0, idx-20):idx+30]
                                words = context.split()
                                for word in words:
                                    if len(word) > 3 and word not in all_keywords:
                                        all_keywords.append(word)
                    print(f"🔍 Enhanced with web search trends")
            except Exception as e:
                print(f"⚠️ Web search skipped: {e}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in all_keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique_keywords.append(kw)
        
        print(f"🔍 Using {len(unique_keywords[:20])} trending keywords for SEO")
        return unique_keywords[:20]
    
    def generate_seo_metadata(self, domain, scenes, custom_description):
        """Generate SEO-optimized title, description, and hashtags using web search for trends"""
        
        # Step 1: Search for trending keywords
        print("🔍 Searching for trending keywords...")
        trending_keywords = self.search_trending_keywords(domain.name, custom_description)
        
        # Prepare scene summary
        scene_summary = ", ".join([s['location'] for s in scenes[:5]])
        
        # Build trending context
        trending_context = ""
        if trending_keywords:
            trending_context = f"""
TRENDING KEYWORDS (from current web search - USE THESE):
{', '.join(trending_keywords)}

IMPORTANT: Incorporate these trending keywords naturally into the title, description, and hashtags.
These are currently popular search terms that will help the video rank higher."""
        
        prompt = f"""You are a metadata writer for "Calm Meridian" — a YouTube channel featuring calming scenic world videos. Tagline: "Where the World Slows Down."

Domain: {domain.name}
Video Features: {scene_summary}
Custom Description: {custom_description if custom_description else 'Cinematic ambient video'}
{trending_context}

Generate YouTube metadata:

1. TITLE (50-70 characters):
   - Cinematic, evocative, curiosity-driven
   - Include "4K" where natural
   - 1-2 relevant emoji max

2. DESCRIPTION (200-350 words):
   Write clean, flowing prose. NO bold markdown headers. NO section labels like "OPENING HOOK", "WHY WATCH", "CALL TO ACTION", "ENGAGEMENT PROMPT". NO "subscribe/like/bell" prompts. NO asking viewers to comment. NO emojis in the body text.
   
   Just write:
   - An evocative opening paragraph that draws the viewer into the scene
   - A paragraph describing the visual journey and what the video features
   - A brief paragraph about the mood/atmosphere and what it's good for (sleep, meditation, relaxation)
   - 3-5 relevant hashtags at the very end
   
   Let the writing speak for itself. Natural, elegant prose — not a YouTube template.

3. HASHTAGS (15-20 tags):
   - Mix of broad and niche
   - Include domain-specific tags
   - No need for #subscribe or #like

4. PRIMARY_KEYWORDS (8-10 keywords):
   - High-search-volume terms for this niche

Return ONLY valid JSON:
{{
  "title": "Title here",
  "description": "Clean prose description here",
  "hashtags": ["#tag1", "#tag2", ...],
  "primary_keywords": ["keyword1", "keyword2", ...]
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a viral YouTube content creator who writes emotionally captivating video descriptions that make viewers feel like they're already experiencing the video. 

Your style is:
- Clean, elegant prose — no markdown bold, no section headers, no emojis in body
- Immersive and sensory (describe what they'll see, hear, feel)
- Poetic but accessible
- NEVER include: call to action, engagement prompts, subscribe/like/bell requests, questions to viewers
- Naturally incorporates keywords without being spammy

Write descriptions that transport viewers into the experience through pure prose. Return only valid JSON."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean markdown formatting
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            seo_data = json.loads(content)
            seo_data["trending_keywords_used"] = trending_keywords  # Store for reference
            print(f"✅ SEO metadata generated with {len(trending_keywords)} trending keywords")
            return seo_data
            
        except Exception as e:
            print(f"⚠️ SEO generation failed: {e}")
            # Return default SEO if generation fails
            return {
                "title": f"{domain.name} 4K | Relaxing Ambient Video | Sleep & Meditation",
                "description": f"Experience the beauty of {domain.name} in this stunning cinematic journey. Perfect for sleep, meditation, study, and relaxation. High-quality 4K video with peaceful ambient sounds.",
                "hashtags": ["#relaxing", "#meditation", "#sleepmusic", "#ambient", "#4k", f"#{domain.name.lower().replace(' ', '')}", "#peaceful", "#calm", "#nature", "#asmr"],
                "primary_keywords": [domain.name, "relaxing video", "sleep music", "meditation", "ambient"],
                "trending_keywords_used": []
            }
    
    def create_image_prompt(self, scene, domain):
        """Create Leonardo AI prompt with domain styling"""
        description = scene['description']
        lighting = scene['lighting']
        elements = ", ".join(scene['key_elements'])
        mood = scene.get('mood', domain.mood_keywords[0])
        
        prompt = f"""{description}. {lighting} lighting. 
        Mood: {mood}. Key elements: {elements}.
        {domain.style_prompt}. Color palette: {', '.join(domain.color_palette)}.
        {self.base_style}. {domain.name} cinematography."""
        
        return prompt.strip()
    
    def generate_image(self, prompt, scene_name, images_dir, progress_callback=None):
        """Generate image using Leonardo AI"""
        image_path = images_dir / f"{scene_name}.jpg"
        
        if image_path.exists():
            return str(image_path)
        
        if progress_callback:
            progress_callback(f"🎨 {scene_name}")
        
        generation_data = {
            "alchemy": False,
            "height": 1080,
            "modelId": "7b592283-e8a7-4c5a-9ba6-d18c31f258b9",
            "contrast": 3.5,
            "num_images": 1,
            "styleUUID": "111dc692-d470-4eec-b791-3475abac4c46",
            "prompt": prompt,
            "width": 1920,
            "ultra": False
        }
        
        response = requests.post(
            f"{self.leonardo_base_url}/generations",
            headers=self.leonardo_headers,
            json=generation_data
        )
        response.raise_for_status()
        
        generation_id = response.json()['sdGenerationJob']['generationId']
        
        for attempt in range(60):
            time.sleep(3)
            
            status_response = requests.get(
                f"{self.leonardo_base_url}/generations/{generation_id}",
                headers=self.leonardo_headers
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            
            if status_data['generations_by_pk']['status'] == 'COMPLETE':
                image_url = status_data['generations_by_pk']['generated_images'][0]['url']
                img_response = requests.get(image_url)
                img_response.raise_for_status()
                
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                
                return str(image_path)
                
            elif status_data['generations_by_pk']['status'] == 'FAILED':
                raise Exception("Image generation failed")
        
        raise Exception("Image generation timeout")
    
    def apply_camera_effect(self, image_path, movement, duration):
        """Apply camera movement effect"""
        img = Image.open(image_path)
        w, h = img.size
        
        if movement == 'zoom_in':
            def make_frame(t):
                progress = t / duration
                zoom = 1.0 + (0.15 * progress)
                new_w, new_h = int(w * zoom), int(h * zoom)
                zoomed = img.resize((new_w, new_h), Image.LANCZOS)
                left, top = (new_w - w) // 2, (new_h - h) // 2
                cropped = zoomed.crop((left, top, left + w, top + h))
                return np.array(cropped)
        
        elif movement == 'zoom_out':
            def make_frame(t):
                progress = t / duration
                zoom = 1.15 - (0.15 * progress)
                new_w, new_h = int(w * zoom), int(h * zoom)
                zoomed = img.resize((new_w, new_h), Image.LANCZOS)
                left, top = (new_w - w) // 2, (new_h - h) // 2
                cropped = zoomed.crop((left, top, left + w, top + h))
                return np.array(cropped)
        
        elif movement == 'pan_right':
            wide_w = int(w * 1.2)
            wide_img = img.resize((wide_w, h), Image.LANCZOS)
            def make_frame(t):
                progress = t / duration
                offset = int((wide_w - w) * progress)
                cropped = wide_img.crop((offset, 0, offset + w, h))
                return np.array(cropped)
        
        elif movement == 'pan_left':
            wide_w = int(w * 1.2)
            wide_img = img.resize((wide_w, h), Image.LANCZOS)
            def make_frame(t):
                progress = t / duration
                offset = int((wide_w - w) * (1 - progress))
                cropped = wide_img.crop((offset, 0, offset + w, h))
                return np.array(cropped)
        
        elif movement == 'tilt_up':
            tall_h = int(h * 1.2)
            tall_img = img.resize((w, tall_h), Image.LANCZOS)
            def make_frame(t):
                progress = t / duration
                offset = int((tall_h - h) * progress)
                cropped = tall_img.crop((0, offset, w, offset + h))
                return np.array(cropped)
        
        else:
            def make_frame(t):
                return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def generate_video(self, domain, duration, custom_description, audio_path, project_folder,
                      use_domain_weights, include_signature, optimize_lighting,
                      progress_callback):
        """Main video generation pipeline"""
        
        # Setup directories
        images_dir = project_folder / "images"
        scenes_dir = project_folder / "scenes"
        images_dir.mkdir(exist_ok=True)
        scenes_dir.mkdir(exist_ok=True)
        
        # Step 1: Generate scene plan
        progress_callback(15, "🧠 AI planning scenes...")
        scenes = self.generate_scene_plan(domain, duration, custom_description, include_signature, optimize_lighting)
        
        # Save scene plan
        plan_path = project_folder / "scene_plan.json"
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump({"domain": domain.name, "scenes": scenes}, f, indent=2)
        
        # Step 2: Generate images
        total_scenes = len(scenes)
        
        for i, scene in enumerate(scenes):
            scene_name = f"scene_{i+1:02d}_{scene['location'].lower().replace(' ', '_')[:30]}"
            prompt = self.create_image_prompt(scene, domain)
            
            # Save scene info
            scene_info_path = scenes_dir / f"{scene_name}_info.json"
            with open(scene_info_path, 'w', encoding='utf-8') as f:
                json.dump({**scene, "prompt": prompt}, f, indent=2)
            
            progress = 15 + int((50 * (i + 1)) / total_scenes)
            progress_callback(progress, f"🎨 Image {i+1}/{total_scenes}: {scene['location']}")
            
            scene['image_path'] = self.generate_image(prompt, scene_name, images_dir)
            scene['duration'] = 10.0
        
        # Step 3: Apply camera effects
        clips = []
        for i, scene in enumerate(scenes):
            progress = 65 + int((20 * (i + 1)) / total_scenes)
            progress_callback(progress, f"🎬 Effect {i+1}/{total_scenes}")
            
            clip = self.apply_camera_effect(
                scene['image_path'],
                scene['camera_movement'],
                scene['duration']
            )
            clips.append(clip)
        
        # Step 4: Assemble video
        progress_callback(85, "🎵 Assembling video...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add audio
        if audio_path and Path(audio_path).exists():
            progress_callback(90, "🎵 Adding music...")
            audio = AudioFileClip(str(audio_path))
            video_duration = final_video.duration
            audio_duration = audio.duration
            
            # If audio is shorter than video, loop it
            if audio_duration < video_duration:
                loops_needed = int(video_duration / audio_duration) + 1
                audio_clips = [audio] * loops_needed
                looped_audio = concatenate_audioclips(audio_clips)
                audio = looped_audio.with_duration(video_duration)
            else:
                # Audio is longer or equal, trim to video duration
                audio = audio.with_duration(video_duration)
            
            # Apply gentle fade out at the end (last 3 seconds)
            fade_duration = min(3.0, video_duration * 0.1)
            try:
                from moviepy.audio.fx import AudioFadeOut
                audio = audio.with_effects([AudioFadeOut(fade_duration)])
            except Exception:
                pass  # Skip fade if not supported
            
            final_video = final_video.with_audio(audio)
        
        # Export
        output_path = project_folder / "final_video.mp4"
        progress_callback(95, "💾 Rendering...")
        
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            bitrate='10000k',
            preset='slow',
            threads=4,
            logger=None
        )
        
        # Cleanup
        for clip in clips:
            clip.close()
        final_video.close()
        
        # Step 5: Generate SEO metadata
        progress_callback(98, "🔍 Generating SEO metadata...")
        seo_metadata = self.generate_seo_metadata(domain, scenes, custom_description)
        
        # Save SEO metadata
        seo_path = project_folder / "seo_metadata.json"
        with open(seo_path, 'w', encoding='utf-8') as f:
            json.dump(seo_metadata, f, indent=2)
        
        return output_path, scenes, seo_metadata
