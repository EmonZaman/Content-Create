"""cholojai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from rest_auth.views import PasswordResetConfirmView
from content_create.settings import env, STATIC_URL, MEDIA_URL, STATIC_ROOT, MEDIA_ROOT

api_url_patterns = (
    [
        path('accounts/v1/', include('accounts.api.v1.urls')),
        path('category/v1/', include('category.api.v1.urls')),
        path('subscriber/v1/', include('subscriber.api.v1.urls')),

    ], 'api'
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('category/', include('category.urls')),
    path('', views.index, name='index'),

    path('api/', include(api_url_patterns)),
    path('api_auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # path('dj-rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #     PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'),
    path('reset-password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

]

if env.str('ENV_TYPE') == 'DEVELOPMENT':
    import debug_toolbar

    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
