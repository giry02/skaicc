from PIL import Image, ImageDraw, ImageFont
import os

# Define assets directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Define configurations
AVATARS = {
    "pm.png": {"color": "#4a90e2", "text": "PM"},
    "pl.png": {"color": "#00bcd4", "text": "PL"},
    "planner.png": {"color": "#4caf50", "text": "PLAN"},
    "designer.png": {"color": "#9c27b0", "text": "DSGN"},
    "publisher.png": {"color": "#ffeb3b", "text": "PUB"},
    "developer.png": {"color": "#f44336", "text": "DEV"},
    "qa.png": {"color": "#ff9800", "text": "QA"},
    "system.png": {"color": "#9e9e9e", "text": "SYS"},
    "user.png": {"color": "#607d8b", "text": "USER"},
    "default.png": {"color": "#ccc", "text": "?"}
}

def create_avatar(filename, settings):
    size = (100, 100)
    img = Image.new('RGB', size, color=settings['color'])
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text position
    text = settings['text']
    # Simple centering estimation as getsize might vary by pillow version
    # d.text((25, 30), text, fill=(255, 255, 255), font=font) 
    
    # improved centering
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2 - 5)
    
    # Use black text for yellow background, white for others
    text_color = "black" if settings['color'] == "#ffeb3b" else "white"
    
    d.text(position, text, fill=text_color, font=font)
    
    save_path = os.path.join(ASSETS_DIR, filename)
    img.save(save_path)
    print(f"Created {save_path}")

if __name__ == "__main__":
    print("Generating placeholder avatars...")
    for filename, settings in AVATARS.items():
        create_avatar(filename, settings)
    print("Done.")
