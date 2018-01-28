from django.contrib import admin
from .models import Profile, Photo, Comment


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photosCount']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'timestamp','commentsCount']
    list_filter = ['timestamp']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'text','updated']
    list_filter = ['updated']



admin.site.register(Photo, ImageAdmin)

admin.site.register(Comment,CommentAdmin)

admin.site.register(Profile, ProfileAdmin)