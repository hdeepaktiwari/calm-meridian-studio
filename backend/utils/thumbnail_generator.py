"""Generate YouTube thumbnails from scene images.

Uses the FIRST image (generated at ultra quality) as the thumbnail base,
with a single calm/peaceful word elegantly centered.
"""
import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# Calm, peaceful single words that evoke tranquility
CALM_WORDS = [
    "Serenity", "Stillness", "Tranquil", "Peaceful", "Harmony",
    "Solace", "Bliss", "Ethereal", "Calm", "Breathe",
    "Silence", "Grace", "Dream", "Gentle", "Radiance",
    "Wonder", "Timeless", "Drift", "Soothe", "Sacred",
    "Infinite", "Luminous", "Whisper", "Sublime", "Zenith",
]


def generate_thumbnail(title: str, images_dir: str, output_path: str) -> str:
    """Generate a 1280x720 thumbnail with the first (best quality) image
    and a single calm word elegantly centered.

    Args:
        title: Video title (used to pick a contextually appropriate word)
        images_dir: Directory containing scene images
        output_path: Where to save the thumbnail

    Returns: output_path
    """
    images_dir = Path(images_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Use the FIRST image (scene_01_*) — it's generated at ultra quality
    image_files = sorted(
        [f for f in images_dir.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp')],
        key=lambda f: f.name,  # scene_01 comes first alphabetically
    )

    if not image_files:
        img = Image.new('RGB', (1280, 720), (20, 10, 30))
    else:
        img = Image.open(image_files[0]).convert('RGB')

    # Resize/crop to 1280x720
    img = _resize_crop(img, 1280, 720)

    # Subtle vignette effect — darken edges to draw focus to center
    img = _apply_vignette(img)

    # Pick a calm word
    word = _pick_word(title)

    # Add the word elegantly centered
    draw = ImageDraw.Draw(img)
    font = _get_elegant_font(72)

    # Measure text
    bbox = font.getbbox(word)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (1280 - text_w) // 2
    y = (720 - text_h) // 2 - 20  # Slightly above true center looks better

    # Soft glow/shadow behind text — draw on separate layer, blur it
    glow_img = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    # Draw solid black text, then blur for glow effect
    glow_draw.text((x, y), word, fill=(0, 0, 0, 160), font=font)
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=12))

    img = img.convert('RGBA')
    img = Image.alpha_composite(img, glow_img)

    # Draw the word in clean white with slight transparency
    text_layer = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    text_draw.text((x, y), word, fill=(255, 255, 255, 240), font=font)
    img = Image.alpha_composite(img, text_layer)

    img = img.convert('RGB')
    img.save(str(output_path), 'JPEG', quality=98)
    return str(output_path)


def _pick_word(title: str) -> str:
    """Pick a contextually appropriate calm word based on title keywords."""
    title_lower = title.lower()

    # Context-aware picks
    if any(w in title_lower for w in ['ocean', 'sea', 'beach', 'coast', 'wave']):
        pool = ["Drift", "Soothe", "Infinite", "Breathe", "Solace"]
    elif any(w in title_lower for w in ['forest', 'tree', 'wood', 'green', 'garden']):
        pool = ["Stillness", "Whisper", "Gentle", "Sacred", "Breathe"]
    elif any(w in title_lower for w in ['mountain', 'himalay', 'peak', 'alpine']):
        pool = ["Zenith", "Sublime", "Timeless", "Ethereal", "Wonder"]
    elif any(w in title_lower for w in ['space', 'cosmic', 'galaxy', 'star', 'nebula']):
        pool = ["Infinite", "Ethereal", "Luminous", "Wonder", "Sublime"]
    elif any(w in title_lower for w in ['temple', 'buddhist', 'sacred', 'spiritual']):
        pool = ["Sacred", "Harmony", "Grace", "Silence", "Calm"]
    elif any(w in title_lower for w in ['palace', 'luxury', 'mansion', 'royal']):
        pool = ["Radiance", "Grace", "Sublime", "Timeless", "Luminous"]
    elif any(w in title_lower for w in ['desert', 'sand', 'dune']):
        pool = ["Solace", "Silence", "Timeless", "Ethereal", "Drift"]
    elif any(w in title_lower for w in ['japan', 'zen', 'bamboo', 'sakura']):
        pool = ["Harmony", "Stillness", "Grace", "Calm", "Gentle"]
    elif any(w in title_lower for w in ['snow', 'winter', 'ice', 'arctic', 'antarc']):
        pool = ["Stillness", "Silence", "Ethereal", "Calm", "Whisper"]
    elif any(w in title_lower for w in ['rain', 'lake', 'river', 'waterfall']):
        pool = ["Soothe", "Gentle", "Drift", "Tranquil", "Serenity"]
    else:
        pool = CALM_WORDS

    return random.choice(pool)


def _apply_vignette(img: Image.Image) -> Image.Image:
    """Apply a subtle vignette to draw focus to center. Uses numpy for speed."""
    import numpy as np

    width, height = img.size
    arr = np.array(img, dtype=np.float32)

    # Create radial gradient mask
    Y, X = np.ogrid[:height, :width]
    cx, cy = width / 2, height / 2
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    max_dist = np.sqrt(cx ** 2 + cy ** 2)
    ratio = dist / max_dist

    # Smooth vignette: starts at 50% radius, max darkening 30%
    vignette = np.clip((ratio - 0.5) / 0.5, 0, 1) * 0.3
    vignette = 1.0 - vignette

    # Apply to all channels
    arr *= vignette[:, :, np.newaxis]
    arr = np.clip(arr, 0, 255).astype(np.uint8)

    return Image.fromarray(arr)


def _resize_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize and center-crop to exact dimensions."""
    ratio = max(target_w / img.width, target_h / img.height)
    img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def _get_elegant_font(size: int):
    """Get an elegant, thin serif or clean font suitable for calm aesthetic."""
    font_paths = [
        # Elegant serif fonts (preferred for calm aesthetic)
        '/System/Library/Fonts/Palatino.ttc',
        '/System/Library/Fonts/Optima.ttc',
        '/System/Library/Fonts/Times.ttc',
        '/System/Library/Fonts/Avenir Next.ttc',
        '/System/Library/Fonts/Avenir.ttc',
        # Fallbacks
        '/System/Library/Fonts/Helvetica.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap_text(text: str, font, max_width: int) -> list[str]:
    """Simple word wrap."""
    words = text.split()
    lines = []
    current = ''
    for word in words:
        test = f'{current} {word}'.strip()
        bbox = font.getbbox(test)
        if bbox[2] > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines or [text]
