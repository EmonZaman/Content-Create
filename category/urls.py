from django.urls import path, include

from .views import *

urlpatterns = [
    # path('',subscription, name='subscription'),
    path('charge/',charge, name='charge'),
    path('create-checkout-session/',CreateCheckoutSessionView.as_view(), name="checkout-session"),
    path('landingpage/',ProductLandingPageView.as_view(),name= "landing-page"),
    path('success/', SuccessView.as_view(), name="success-page"),
    path('cancel/', CancelView.as_view(), name="cancel-page"),

]