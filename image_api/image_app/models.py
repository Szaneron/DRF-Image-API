from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.html import escape


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
