from django.contrib import admin
from .models import Subscriber


# Register your models here.

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass
