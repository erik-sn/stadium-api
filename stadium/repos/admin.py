from django.contrib import admin


from .models import Repo


@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = ('name', 'owner', 'html_url', 'private', 'license', 'created', 'last_updated')

    fields = ('pypi_url', 'pypi_name', 'created', 'last_updated', 'name', 'owner', 'html_url',
              'private', 'license', 'readme', 'api_url', 'github_id', 'git_url', 'ssh_url', 'forks',
              'stargazers_count', 'size', 'fork', 'description', 'homepage', 'full_name')
    readonly_fields = ('created', 'last_updated', 'name', 'owner', 'html_url', 'private', 'license',
                       'readme', 'api_url', 'github_id', 'git_url', 'ssh_url', 'forks',
                       'stargazers_count', 'size', 'fork', 'description', 'homepage', 'full_name')

    search_fields = ['owner__username', 'name']
    list_filter = ('private', 'fork')

    def has_add_permission(self, request, obj=None):
        return False
