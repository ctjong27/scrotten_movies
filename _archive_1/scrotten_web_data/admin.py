from django.contrib import admin
from .models import ScrottenWebData


class ScrottenWebDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScrottenWebData, ScrottenWebDataAdmin)