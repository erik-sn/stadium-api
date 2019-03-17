from django.contrib import admin


from .models import ProjectAuthor


@admin.register(ProjectAuthor)
class ProjectAuthorAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('id', 'full_name', 'github_id', 'login', 'html_url', 'avatar_url', 'created', 'last_updated')

    fields = ('full_name', 'github_id', 'login', 'html_url', 'avatar_url', 'created', 'last_updated')
    readonly_fields = ('created', 'last_updated')

    search_fields = ['full_name', 'login']