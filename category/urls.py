from django.urls import path, include

from .views import *

urlpatterns = [
    path('',subscription, name='subscription'),
    path('charge/',charge, name='charge')
]