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
from django.urls import path, include

from content_create.settings import env, STATIC_URL, MEDIA_URL, STATIC_ROOT, MEDIA_ROOT

api_url_patterns = (
    [
        path('accounts/v1/', include('accounts.api.v1.urls')),
        path('category/v1/', include('category.api.v1.urls')),

    ], 'api'
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(api_url_patterns)),
    path('api_auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
]

if env.str('ENV_TYPE') == 'DEVELOPMENT':
    import debug_toolbar

    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
