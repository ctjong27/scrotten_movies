from django.contrib import admin
from .models import ScrottenMovie

class ScrottenMovieAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScrottenMovie, ScrottenMovieAdmin)