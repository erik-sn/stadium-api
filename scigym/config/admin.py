from django.contrib import admin

from .models import ImageConfig


@admin.register(ImageConfig)
class ImageConfigAdmin(admin.ModelAdmin):
    list_display = ('valid_image_formats',)

    fields = ('valid_image_formats',)

