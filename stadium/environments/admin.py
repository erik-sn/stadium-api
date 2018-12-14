from django.contrib import admin

from .models import Environment


@admin.register(Environment)
class EnvAdmin(admin.ModelAdmin):
    pass
