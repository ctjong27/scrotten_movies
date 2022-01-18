from django.contrib import admin
from .models import ScrottenWebData


class ScrottenMovieToMemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScrottenWebData, ScrottenWebDataAdmin)