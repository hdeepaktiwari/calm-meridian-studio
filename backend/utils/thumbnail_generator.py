"""Generate YouTube thumbnails from scene images."""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def generate_thumbnail(title: str, images_dir: str, output_path: str) -> str:
    """Generate a 1280x720 thumbnail with gradient overlay and title text.

    Args:
        title: Video title to overlay
        images_dir: Directory containing scene images
        output_path: Where to save the thumbnail

    Returns: output_path
    """
    images_dir = Path(images_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Find best image (largest file = usually highest quality)
    image_files = sorted(
        [f for f in images_dir.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp')],
        key=lambda f: f.stat().st_size,
        reverse=True,
    )

    if not image_files:
        # Create a dark placeholder
        img = Image.new('RGB', (1280, 720), (20, 10, 30))
    else:
        img = Image.open(image_files[0]).convert('RGB')

    # Resize/crop to 1280x720
    img = _resize_crop(img, 1280, 720)

    # Add dark gradient overlay at bottom
    overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    for y in range(360, 720):
        alpha = int(200 * (y - 360) / 360)
        draw_overlay.line([(0, y), (1280, y)], fill=(0, 0, 0, alpha))

    img = img.convert('RGBA')
    img = Image.alpha_composite(img, overlay).convert('RGB')

    # Add title text
    draw = ImageDraw.Draw(img)
    font = _get_font(48)

    # Word wrap
    lines = _wrap_text(title, font, 1200)
    text_block = '\n'.join(lines[-3:])  # Max 3 lines

    y_start = 720 - 60 - (len(lines[-3:]) * 58)
    for i, line in enumerate(lines[-3:]):
        y = y_start + i * 58
        # Shadow
        draw.text((42, y + 2), line, fill=(0, 0, 0), font=font)
        draw.text((40, y), line, fill=(255, 255, 255), font=font)

    img.save(str(output_path), 'JPEG', quality=95)
    return str(output_path)


def _resize_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize and center-crop to exact dimensions."""
    ratio = max(target_w / img.width, target_h / img.height)
    img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def _get_font(size: int):
    """Try to get a nice bold font, fall back to default."""
    font_paths = [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/SFNSDisplay-Bold.otf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
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
