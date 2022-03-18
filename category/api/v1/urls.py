from django.urls import path
from category.api.v1.views import CategoryDetailAPIView, CategoryListApiView, VideoListApiView, VideoDetailAPIView, \
    category_content

urlpatterns = [
    path('items/', CategoryListApiView.as_view(), name="category_list"),
    path('items/<int:pk>/', CategoryDetailAPIView.as_view(), name="category_list_individual"),
    path('video/', VideoListApiView.as_view(), name="video_list"),
    path('video/<int:pk>/', VideoDetailAPIView.as_view(), name="video_list_individual"),
    path('video_category/', category_content.as_view(), name="video_catgory")
]
