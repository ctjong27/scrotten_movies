from django.contrib import admin
from .models import ScrottenMovieToMember


class ScrottenMovieToMemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScrottenMovieToMember, ScrottenMovieToMemberAdmin)