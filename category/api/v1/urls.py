from django.urls import path
from category.api.v1.views import CategoryDetailAPIView, CategoryListApiView, VideoListApiView, VideoDetailAPIView, \
    LastSevenDaysUserListAPIView, LastSevenDaySubscriberListAPIView, UserAndSubscriberCountAPIView, \
    category_content_count, StripeCreateCheckoutSessionAPIView, LikeUpdate, SaveVideosUpdate, \
    StripeSuccessAPIView,RecentVideosUpdate

urlpatterns = [
    path('categories/', CategoryListApiView.as_view(), name="category_list"),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name="category_list_individual"),
    path('video/', VideoListApiView.as_view(), name="video_list"),
    path('video/<int:pk>/', VideoDetailAPIView.as_view(), name="video_list_individual"),
    path('video/like/<int:pk>/', LikeUpdate.as_view(), name='video_likes'),
    # path('video/like/', Like.as_view(), name='video_likes'),
    path('save/video/<int:pk>/', SaveVideosUpdate.as_view(), name='video_likes'),
    path('recent/video/<int:pk>/', RecentVideosUpdate.as_view(), name='video_likes'),

    # path('videos_by_category/', category_content.as_view(), name="video_category"),
    path('videos_by_category_count/', category_content_count.as_view(), name="video_category"),

    path('last_seven_days_user_list/', LastSevenDaysUserListAPIView.as_view(), name="Last seven Days user list"),
    path('last_seven_subscriber_list/', LastSevenDaySubscriberListAPIView.as_view(),
         name="Last seven Days Subscriber list"),
    path('count/', UserAndSubscriberCountAPIView.as_view(),
         name="Detail Count"),
    path('create-checkout-session/', StripeCreateCheckoutSessionAPIView.as_view(), name="checkout-session_api"),
    path('session-check/', StripeSuccessAPIView.as_view(), name="checkout-session_check"),

    # path('webhooks/stripe', stripe_webhook_view, name="stripe_webhook-api"),
]
