from django.contrib import admin

from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'name', 'description', 'file_path', 'hash', 'created')
    fields = ('name', 'description')
    readonly_fields = ('created', 'last_updated', 'file_path', 'hash')