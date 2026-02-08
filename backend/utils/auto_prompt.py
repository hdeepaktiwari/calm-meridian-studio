"""
Auto-prompt generator using GPT-4o-mini for unique video descriptions.
"""
import os
import random
from typing import Optional

def generate_auto_prompt(domain, duration: int, variation_index: int = 0) -> str:
    """Generate a unique prompt for a domain using GPT-4o-mini."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception:
        return _fallback_prompt(domain, duration, variation_index)

    # Randomly select subsets for variety
    locations = random.sample(domain.locations, min(3, len(domain.locations)))
    elements = random.sample(domain.signature_elements, min(4, len(domain.signature_elements)))
    lighting = random.choice(domain.lighting_conditions)
    moods = random.sample(domain.mood_keywords, min(3, len(domain.mood_keywords)))
    colors = random.sample(domain.color_palette, min(2, len(domain.color_palette)))

    variation_seeds = [
        "Focus on dawn lighting with soft golden rays",
        "Focus on moonlit atmosphere with deep shadows",
        "Emphasize aerial perspectives and vast scale",
        "Highlight intimate close-up details and textures",
        "Capture the transition from day to night",
        "Focus on misty, ethereal atmosphere",
        "Emphasize dramatic contrasts and bold compositions",
        "Highlight serene stillness and peaceful moments",
        "Focus on movement and flowing elements",
        "Capture the interplay of light and shadow",
    ]
    seed = variation_seeds[variation_index % len(variation_seeds)]

    dur_label = f"{duration // 60} minute"

    system_msg = (
        "You are a cinematic video description writer. Generate a unique, vivid description "
        "for an AI-generated relaxation/ambient video. The description should be 2-3 sentences, "
        "evocative and specific. Do NOT include titles or hashtags, just the scene description."
    )

    user_msg = (
        f"Domain: {domain.name}\n"
        f"Duration: {dur_label}\n"
        f"Locations to feature: {', '.join(locations)}\n"
        f"Visual elements: {', '.join(elements)}\n"
        f"Lighting: {lighting}\n"
        f"Mood: {', '.join(moods)}\n"
        f"Color palette: {', '.join(colors)}\n"
        f"Creative direction: {seed}\n\n"
        f"Write a unique cinematic scene description for this video."
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=200,
            temperature=0.9,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return _fallback_prompt(domain, duration, variation_index)


def _fallback_prompt(domain, duration: int, variation_index: int = 0) -> str:
    """Fallback prompt without API call."""
    locations = random.sample(domain.locations, min(2, len(domain.locations)))
    elements = random.sample(domain.signature_elements, min(3, len(domain.signature_elements)))
    lighting = random.choice(domain.lighting_conditions)
    mood = random.choice(domain.mood_keywords)

    return (
        f"A {mood} cinematic journey through {domain.name.lower()} featuring "
        f"{', '.join(locations).lower()} with {', '.join(elements).lower()}, "
        f"captured in {lighting} for a deeply immersive {duration // 60}-minute experience."
    )
