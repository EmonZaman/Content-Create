from django.contrib import admin
from .models import Category, Video, UserSubscription, VideoLikes, SaveVideos, RecentShownVideos


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoLikes)
class VideoLikesAdmin(admin.ModelAdmin):
    pass


@admin.register(SaveVideos)
class SaveVideosAdmin(admin.ModelAdmin):
    pass


@admin.register(RecentShownVideos)
class RecentShownVideosAdmin(admin.ModelAdmin):
    pass
