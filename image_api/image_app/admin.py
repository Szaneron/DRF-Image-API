from django.contrib import admin

# Register your models here.
from rest_framework.authtoken.admin import TokenAdmin
from .models import Image

admin.site.register(Image)
TokenAdmin.raw_id_fields = ['user']
