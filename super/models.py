import os
import time
import uuid
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


def product_image_upload_path(instance, filename):
    ext = Path(filename).suffix.lower() or ".jpg"
    timestamp = int(time.time() * 1000)
    unique = uuid.uuid4().hex[:8]
    return f"static/media/products/{timestamp}_{unique}{ext}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_upload_path)
    thumbnail = models.ImageField(upload_to="static/media/products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_image_uploaded = False

        if self.pk:
            old = Product.objects.filter(pk=self.pk).only("image").first()
            if old and old.image != self.image:
                new_image_uploaded = True
        else:
            new_image_uploaded = bool(self.image)

        super().save(*args, **kwargs)

        if new_image_uploaded and self.image:
            self.generate_thumbnail()
            super().save(update_fields=["thumbnail"])

    def generate_thumbnail(self, size=(72, 72)):
        img = Image.open(self.image)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, format="JPEG", quality=85)

        timestamp = int(time.time() * 1000)
        unique = uuid.uuid4().hex[:8]
        thumb_name = f"thumbs/{timestamp}_{unique}_thumb.jpg"

        self.thumbnail.save(
            thumb_name,
            ContentFile(thumb_io.getvalue()),
            save=False
        )

    def delete(self, *args, **kwargs):
        """
        Delete DB row + remove image files from storage.
        """
        storage = self.image.storage if self.image else None

        image_name = self.image.name if self.image else None
        thumb_name = self.thumbnail.name if self.thumbnail else None

        super().delete(*args, **kwargs)

        if storage:
            if image_name and storage.exists(image_name):
                storage.delete(image_name)

            if thumb_name and storage.exists(thumb_name):
                storage.delete(thumb_name)
