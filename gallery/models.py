from django.db import models
from PIL import Image, ImageDraw, ImageFont
import os

class GalleryImage(models.Model):
    # --- FIXED: Added Curation Category Matrix ---
    CATEGORY_CHOICES = [
        ('LANDSCAPE', 'Landscapes'),
        ('PORTRAIT', 'Portraits'),
        ('ARCHITECTURAL', 'Architectural'),
    ]

    title = models.CharField(max_length=200, blank=True)
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='LANDSCAPE'
    )
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Plate #{self.pk}"
    # Inside your models.py GalleryImage class:
    @property
    def safe_title(self):
        return self.title if self.title and self.title.strip() else "Untitled Composition"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            base_image = Image.open(img_path).convert("RGBA")
            
            txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            watermark_text = "SAGE"
            sub_text = "GALLERY & PHOTOGRAPHY"
            
            # --- FIXED: Increased scale factors for higher visibility ---
            font_size_main = max(int(base_image.width * 0.06), 32)  # Increased from 0.04
            font_size_sub = max(int(base_image.width * 0.02), 12)   # Increased from 0.015
                
            try:
                font_main = ImageFont.truetype("timesi.ttf", font_size_main) 
                font_sub = ImageFont.truetype("arial.ttf", font_size_sub)
            except IOError:
                font_main = ImageFont.load_default()
                font_sub = ImageFont.load_default()

            bbox_main = draw.textbbox((0, 0), watermark_text, font=font_main)
            w_main, h_main = bbox_main[2] - bbox_main[0], bbox_main[3] - bbox_main[1]
            
            bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
            w_sub, h_sub = bbox_sub[2] - bbox_sub[0], bbox_sub[3] - bbox_sub[1]
            
            max_w = max(w_main, w_sub)
            
            # Margins away from borders
            x_pos = base_image.width - max_w - 50
            y_pos_main = base_image.height - h_main - h_sub - 60
            y_pos_sub = y_pos_main + h_main + 12

            # --- FIXED: Stronger shadow offset & heavier alpha density (180 instead of 80) ---
            shadow_offset = max(2, int(base_image.width * 0.002))
            draw.text((x_pos + shadow_offset, y_pos_main + shadow_offset), watermark_text, fill=(0, 0, 0, 180), font=font_main)
            draw.text((x_pos + shadow_offset, y_pos_sub + shadow_offset), sub_text, fill=(0, 0, 0, 180), font=font_sub)
            
            # --- FIXED: Brightened crisp white text layers (240 out of 255) ---
            draw.text((x_pos, y_pos_main), watermark_text, fill=(255, 255, 255, 240), font=font_main)
            draw.text((x_pos, y_pos_sub), sub_text, fill=(255, 255, 255, 200), font=font_sub)
            
            finished_image = Image.alpha_composite(base_image, txt_layer).convert("RGB")
            finished_image.save(img_path, "JPEG", quality=95)