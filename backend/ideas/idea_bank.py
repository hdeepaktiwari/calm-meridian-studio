"""
Idea Bank - Manages a bank of video ideas for autonomous generation.
Uses GPT-4o-mini to generate unique ideas across all 20 domains.
"""
import os
import json
import uuid
import random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
from typing import Optional

from domains import DOMAIN_REGISTRY

IDEAS_FILE = Path("ideas_bank.json")

# Generation progress tracking
_generation_progress = {"active": False, "generated": 0, "total": 0, "error": None}


def _load_data() -> dict:
    if IDEAS_FILE.exists():
        try:
            with open(IDEAS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"ideas": [], "generation_history": []}


def _save_data(data: dict):
    with open(IDEAS_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


class IdeaBank:
    """Manages a bank of video ideas for autonomous generation."""

    def get_stats(self) -> dict:
        data = _load_data()
        ideas = data["ideas"]
        return {
            "total": len(ideas),
            "available": sum(1 for i in ideas if i["status"] == "available"),
            "used": sum(1 for i in ideas if i["status"] == "used"),
            "scheduled": sum(1 for i in ideas if i["status"] == "scheduled"),
        }

    def get_available_ideas(self, limit: int = 10) -> list:
        data = _load_data()
        available = [i for i in data["ideas"] if i["status"] == "available"]
        return available[:limit]

    def get_all_ideas(self, status: Optional[str] = None) -> list:
        data = _load_data()
        if status:
            return [i for i in data["ideas"] if i["status"] == status]
        return data["ideas"]

    def pick_idea(self) -> Optional[dict]:
        """Pick one available idea using strict round-robin across domains.
        
        Maintains a domain_index that cycles through all domains in order.
        If the next domain has no available ideas, skip to the one after, etc.
        """
        from domains import DOMAIN_REGISTRY
        
        data = _load_data()
        available = [i for i in data["ideas"] if i["status"] == "available"]
        if not available:
            return None

        domain_names = list(DOMAIN_REGISTRY.keys())
        num_domains = len(domain_names)
        
        # Get current round-robin index
        domain_index = data.get("shorts_domain_index", 0)
        
        # Try each domain in order starting from current index
        for offset in range(num_domains):
            idx = (domain_index + offset) % num_domains
            target_domain = domain_names[idx]
            candidates = [i for i in available if i["domain"] == target_domain]
            if candidates:
                picked = random.choice(candidates)
                picked["status"] = "scheduled"
                # Advance index to NEXT domain for next pick
                data["shorts_domain_index"] = (idx + 1) % num_domains
                _save_data(data)
                return picked
        
        # Fallback: pick any available (shouldn't happen if ideas exist)
        picked = random.choice(available)
        picked["status"] = "scheduled"
        data["shorts_domain_index"] = (domain_index + 1) % num_domains
        _save_data(data)
        return picked

    def mark_used(self, idea_id: str, job_id: str):
        data = _load_data()
        for idea in data["ideas"]:
            if idea["id"] == idea_id:
                idea["status"] = "used"
                idea["used_at"] = datetime.now().isoformat()
                idea["video_job_id"] = job_id
                break
        _save_data(data)

    async def generate_ideas(self, count: int = 100) -> int:
        """Generate ideas using GPT-4o-mini in batches of 20."""
        global _generation_progress
        _generation_progress = {"active": True, "generated": 0, "total": count, "error": None}

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            data = _load_data()
            existing_titles = {i["title"].lower() for i in data["ideas"]}
            domain_names = list(DOMAIN_REGISTRY.keys())

            total_generated = 0
            batches = (count + 19) // 20  # ceil division

            for batch_num in range(batches):
                batch_size = min(20, count - total_generated)
                # Distribute across domains
                batch_domains = []
                for i in range(batch_size):
                    idx = (total_generated + i) % len(domain_names)
                    batch_domains.append(domain_names[idx])

                domain_list = ", ".join(set(batch_domains))
                existing_sample = list(existing_titles)[:50]  # Don't send too many

                prompt = f"""Generate {batch_size} unique YouTube Shorts video ideas for a calm/ambient visual channel called "Calm Meridian". 
Each idea MUST be for one of these specific domains: {domain_list}

Requirements:
- Each idea needs a compelling hook line (1 sentence that makes scrollers stop, e.g. "You haven't taken a deep breath in hours")
- Mood should be one of: serene, mysterious, majestic, peaceful, ethereal, dreamy, tranquil, meditative
- Visual keywords should be 4-6 specific visual elements
- No narration - these are visual-only ambient videos
- No duplicate concepts with these existing titles: {existing_sample[:20]}

Return ONLY a JSON array (no markdown, no explanation) where each item has:
{{"domain": "exact domain name", "title": "unique title", "description": "2-3 sentence visual description", "hook_line": "compelling hook", "mood": "mood word", "visual_keywords": ["word1", "word2", "word3", "word4"]}}"""

                try:
                    response = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.9,
                        max_tokens=4000,
                    )
                    content = response.choices[0].message.content.strip()
                    # Clean potential markdown wrapping
                    if content.startswith("```"):
                        content = content.split("\n", 1)[1]
                        if content.endswith("```"):
                            content = content[:-3]
                    
                    ideas_list = json.loads(content)

                    for idea_data in ideas_list:
                        title = idea_data.get("title", "")
                        if title.lower() in existing_titles:
                            continue
                        # Validate domain
                        domain = idea_data.get("domain", "")
                        if domain not in DOMAIN_REGISTRY:
                            # Try to find closest match
                            for d in domain_names:
                                if d.lower() in domain.lower() or domain.lower() in d.lower():
                                    domain = d
                                    break
                            else:
                                domain = random.choice(domain_names)

                        new_idea = {
                            "id": str(uuid.uuid4()),
                            "domain": domain,
                            "title": title,
                            "description": idea_data.get("description", ""),
                            "hook_line": idea_data.get("hook_line", ""),
                            "mood": idea_data.get("mood", "serene"),
                            "visual_keywords": idea_data.get("visual_keywords", []),
                            "status": "available",
                            "created_at": datetime.now().isoformat(),
                            "used_at": None,
                            "video_job_id": None,
                        }
                        data["ideas"].append(new_idea)
                        existing_titles.add(title.lower())
                        total_generated += 1

                    _generation_progress["generated"] = total_generated
                except Exception as e:
                    print(f"Batch {batch_num} failed: {e}")
                    continue

            data["generation_history"].append({
                "generated_at": datetime.now().isoformat(),
                "count": total_generated,
                "batch": batches,
            })
            _save_data(data)
            _generation_progress = {"active": False, "generated": total_generated, "total": count, "error": None}
            return total_generated

        except Exception as e:
            _generation_progress = {"active": False, "generated": 0, "total": count, "error": str(e)}
            raise

    @staticmethod
    def get_generation_progress() -> dict:
        return dict(_generation_progress)
