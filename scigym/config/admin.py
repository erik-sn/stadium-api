from django.contrib import admin

from .models import ImageConfig


@admin.register(ImageConfig)
class ImageAdmin(admin.ModelAdmin):
    pass
