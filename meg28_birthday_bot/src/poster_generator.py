import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging

def get_drive_direct_link(url):
    if 'drive.google.com' in url:
        file_id = ""
        if 'id=' in url:
            file_id = url.split('id=')[-1].split('&')[0]
        elif '/d/' in url:
            file_id = url.split('/d/')[-1].split('/')[0]
        if file_id:
            return f'https://drive.google.com/uc?export=download&id={file_id}'
    return url

def generate_birthday_poster(person, template_path, output_path, font_path):
    try:
        # 1. Load Template (Ensure it has a transparent hole in the middle!)
        # If your template is NOT transparent, this will cover the photo.
        template = Image.open(template_path).convert("RGBA")
        t_width, t_height = template.size

        # 2. Process Celebrant Image
        pic_url = get_drive_direct_link(person['picture_link'])
        response = requests.get(pic_url, timeout=15)
        celebrant_img = Image.open(BytesIO(response.content)).convert("RGBA")

        # 3. RESIZE PHOTO (Slightly larger to ensure it fills the frame)
        # Based on your misaligned output, we need a wider crop.
        photo_width = 480 
        photo_height = 580
        celebrant_img = celebrant_img.resize((photo_width, photo_height), Image.LANCZOS)
        
        # 4. CREATE THE SANDWICH (Layering)
        # Create a white background same size as template
        canvas = Image.new("RGBA", (t_width, t_height), (255, 255, 255, 255))
        
        # Paste the photo onto the canvas FIRST
        # Shifted left (to 300) and slightly up (to 280) to align with the frame
        canvas.paste(celebrant_img, (300, 280))

        # Paste the template ON TOP of the photo
        # This makes the balloons and the white frame borders sit above the face
        final_poster = Image.alpha_composite(canvas, template)

        # 5. Add the Name
        draw = ImageDraw.Draw(final_poster)
        try:
            name_font = ImageFont.truetype(font_path, 75)
        except:
            name_font = ImageFont.load_default()

        full_name = f"{person['first_name']} {person['surname']}".upper()
        
        # Name placement at the bottom
        draw.text((t_width // 2, 940), full_name, font=name_font, fill="white", anchor="mm")

        # 6. Save
        final_poster.convert("RGB").save(output_path, "JPEG", quality=95)
        return output_path

    except Exception as e:
        logging.error(f"Alignment fix failed: {e}")
        return None