import os
from PIL import Image, ImageDraw

def create_icon(size, path):
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate dimensions
    center = size // 2
    padding = size // 10
    radius = center - padding
    
    # Draw soft shadow (simulate premium iOS depth)
    shadow_offset = size // 40
    draw.ellipse(
        [padding, padding + shadow_offset, size - padding, size - padding + shadow_offset],
        fill=(0, 0, 0, 15)
    )
    
    # Draw indigo circle base (#5856D6)
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=(88, 86, 214, 255)
    )
    
    # Draw secondary soft ring inside
    inner_padding = padding + (size // 20)
    draw.ellipse(
        [inner_padding, inner_padding, size - inner_padding, size - inner_padding],
        outline=(255, 255, 255, 40),
        width=max(1, size // 60)
    )
    
    # Draw compass diamond/needle (Adventure/Odyssey theme)
    # Top point
    p_top = (center, inner_padding + (size // 8))
    # Bottom point
    p_bottom = (center, size - inner_padding - (size // 8))
    # Left point
    p_left = (inner_padding + (size // 8), center)
    # Right point
    p_right = (size - inner_padding - (size // 8), center)
    
    # Draw North needle (White)
    draw.polygon([p_top, p_right, (center, center)], fill=(255, 255, 255, 255))
    draw.polygon([p_top, p_left, (center, center)], fill=(255, 255, 255, 200))
    
    # Draw South needle (Rose/Orange Accent #FF9500)
    draw.polygon([p_bottom, p_right, (center, center)], fill=(255, 149, 0, 255))
    draw.polygon([p_bottom, p_left, (center, center)], fill=(255, 149, 0, 200))
    
    # Draw center pin
    pin_radius = size // 24
    draw.ellipse(
        [center - pin_radius, center - pin_radius, center + pin_radius, center + pin_radius],
        fill=(255, 255, 255, 255)
    )
    
    # Save image
    img.save(path, 'PNG')
    print(f"Generated PWA icon: {path} ({size}x{size})")

if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iris-quest")
    os.makedirs(target_dir, exist_ok=True)
    
    create_icon(192, os.path.join(target_dir, "icon.png"))
    create_icon(512, os.path.join(target_dir, "icon-512.png"))
