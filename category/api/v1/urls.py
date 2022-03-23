from django.urls import path
from category.api.v1.views import CategoryDetailAPIView, CategoryListApiView, VideoListApiView, VideoDetailAPIView, \
    category_content, LastSevenDaysUserListAPIView, LastSevenDaySubscriberListAPIView, UserAndSubscriberCountAPIView

urlpatterns = [
    path('categories/', CategoryListApiView.as_view(), name="category_list"),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name="category_list_individual"),
    path('video/', VideoListApiView.as_view(), name="video_list"),
    path('video/<int:pk>/', VideoDetailAPIView.as_view(), name="video_list_individual"),
    path('videos_by_category/', category_content.as_view(), name="video_category"),

    path('last_seven_days_user_list/', LastSevenDaysUserListAPIView.as_view(), name="Last seven Days user list"),
    path('last_seven_subscriber_list/', LastSevenDaySubscriberListAPIView.as_view(), name="Last seven Days Subscriber list"),
    path('count/', UserAndSubscriberCountAPIView.as_view(),
         name="Detail Count"),

]
