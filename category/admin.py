from django.contrib import admin
from .models import Category, Video, UserSubcription
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSubcription)
class UserSubcriptionAdmin(admin.ModelAdmin):
    pass

