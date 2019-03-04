from django.contrib import admin

from .models import Environment, Topic


@admin.register(Environment)
class EnvAdmin(admin.ModelAdmin):
    pass

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('name', 'id', 'parent_topic')

    fields = ('name', 'parent_topic')

    search_fields = ['name']
