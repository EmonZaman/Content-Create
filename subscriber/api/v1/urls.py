from django.urls import path

from subscriber.api.v1.views import SubscriberListAPIView, SubscriberDetailAPIView

urlpatterns = [

    path('subscriberlist/', SubscriberListAPIView.as_view(), name="subscriber_list"),
    path('subscriberlist/<int:pk>/',SubscriberDetailAPIView.as_view(), name= "subscriber_list_individual" )

]