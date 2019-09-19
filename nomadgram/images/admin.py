from django.contrib import admin

from nomadgram.images.models import *


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['location', 'creator__name', 'file']
    list_filter = ('location', )
    list_display_links = ('location','caption',)
    list_display = (
        'file',
        'location',
        'caption',
        'creator',
        'created_at',
        'updated_at',
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'creator',
        'image',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'message',
        'creator',
        'image',
        'created_at',
        'updated_at',
    )
