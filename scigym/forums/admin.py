from django.contrib import admin

from .models import MessageBoard, Comment


@admin.register(MessageBoard)
class MessageBoardAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('title', 'title_url', 'description', 'tags', 'author', 'environment')

    fields = ('title', 'title_url', 'description', 'tags', 'author', 'environment')

    search_fields = ['title', 'title_url', 'description', 'tags', 'author', 'environment']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('comment', 'author', 'board')

    fields = ('comment', 'author', 'board')

    search_fields = ['comment', 'author', 'board']
    