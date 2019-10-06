from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'name', 'file_path', 'owner', 'created')
    fields = ('name',)
    readonly_fields = ('created', 'last_updated', 'file_path', 'owner')
