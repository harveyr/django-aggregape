from django.contrib import admin
from . import models


class GithubFeedAdmin(admin.ModelAdmin):
    list_display = ['username']
    fields = ['username', 'token', 'api_key']
    search_fields = ['username']

admin.site.register(models.GithubFeed, GithubFeedAdmin)
