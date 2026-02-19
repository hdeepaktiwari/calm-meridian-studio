"""
Ambient sound management for Shorts.
MVP: fallback to existing music at low volume or silence.
"""
import json
import random
from pathlib import Path
from typing import Optional

AMBIENT_LIBRARY_FILE = Path(__file__).parent.parent / "music" / "ambient_library.json"
MUSIC_DIR = Path(__file__).parent.parent / "music"

# Domain → ambient category mapping
_DOMAIN_AMBIENT = {
    "Ocean & Sea Creatures": ["ocean"],
    "Beautiful Beaches": ["ocean", "wind"],
    "Lush Green Forests": ["forest", "birds", "stream"],
    "Beautiful Himalayas": ["wind", "stream", "birds"],
    "Amazon Rainforest": ["forest", "rain", "birds"],
    "Lakeside Lifestyle": ["stream", "birds", "wind"],
    "Tropical Greenery": ["rain", "forest", "birds"],
    "Buddhist Lifestyle": ["wind", "stream"],
    "Japanese Beauty": ["stream", "birds", "wind"],
    "Antarctica Beauty": ["wind", "ocean"],
    "Desert Life Worldwide": ["wind", "night"],
    "Life in Space": ["night"],
    "Ancient Places": ["wind", "night"],
    "Ancient European Cities": ["wind", "rain"],
}


def load_ambient_library() -> list[dict]:
    if AMBIENT_LIBRARY_FILE.exists():
        with open(AMBIENT_LIBRARY_FILE) as f:
            data = json.load(f)
        return data.get("ambient", [])
    return []


def get_ambient_for_domain(domain_name: str) -> Optional[str]:
    """Get an ambient sound file path for a domain. Returns None if no files available."""
    library = load_ambient_library()
    if not library:
        return None

    categories = _DOMAIN_AMBIENT.get(domain_name, [])
    # Filter by category
    candidates = [a for a in library if a.get("category") in categories]
    if not candidates:
        candidates = library

    for candidate in random.sample(candidates, min(3, len(candidates))):
        path = MUSIC_DIR / candidate["filename"]
        if path.exists():
            return str(path)

    return None


def get_fallback_music() -> Optional[str]:
    """Get the shortest existing music track as fallback."""
    library_file = MUSIC_DIR / "music_library.json"
    if not library_file.exists():
        return None
    with open(library_file) as f:
        lib = json.load(f)
    short_tracks = lib.get("short", [])
    if not short_tracks:
        return None
    # Pick the shortest
    shortest = min(short_tracks, key=lambda t: t["duration_seconds"])
    path = MUSIC_DIR / shortest["filename"]
    return str(path) if path.exists() else None
