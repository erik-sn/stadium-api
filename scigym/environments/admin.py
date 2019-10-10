from django.contrib import admin

from .models import Environment, Topic


@admin.register(Environment)
class EnvAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('name', 'description', 'scigym', 'repository', 'tags', 'topic', 'current_avatar')

    fields = ('name', 'description', 'scigym', 'current_avatar')

    search_fields = ['name', 'repository']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('name', 'id', 'parent_topic')

    fields = ('name', 'parent_topic')

    search_fields = ['name']
