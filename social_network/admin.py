from django.contrib import admin
from .models import Tweet, Comment, Like

# Register your models here.
class TweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'user']
    search_fields = ['text']
    list_filter=['user']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tweet', 'comment', 'parent']
    search_fields=['comment']
    list_filter=['user', 'tweet']


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'like']
    search_fields=['user']
    list_filter=['user']

admin.site.register(Tweet, TweetAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)