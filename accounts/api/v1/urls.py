from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserListApiView, UserDetailAPIView, RegisterAPIView, LoginAPIView, CurrentUser, GoogleLoginView


urlpatterns = [
    path('userlist/', UserListApiView.as_view(), name="user"),
    path('userlist/<int:pk>/', UserDetailAPIView.as_view(), name="user_detail"),
    path('register/',RegisterAPIView.as_view(),name="register"),
    path('login/',LoginAPIView.as_view(),name="login"),
    path('current_user/',CurrentUser.as_view(),name="current-user"),
    path('google/login/',GoogleLoginView.as_view(),name="google-log-in"),
    # path('user/profile/', UserProfileDetailApiView.as_view(), name="user-profile"),

]





