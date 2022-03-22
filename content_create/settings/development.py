import os

import django_heroku
from .defaults import *

DEBUG = True

ALLOWED_HOSTS = ['django-testing-app-check.herokuapp.com', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'


# STATIC_ROOT = BASE_DIR / 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_DIRS = [BASE_DIR / 'static_local']
# storage for cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# storage for aws s3
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DEBUG TOOLBAR
INTERNAL_IPS = ['127.0.0.1']
# Activate Django-Heroku.
django_heroku.settings(locals())
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dlvdomgmh',
    'API_KEY': '424831393245899',
    # 'resource_type':'video',
    'API_SECRET': 'drO3KapwEEH_qXQTI9UZp-231Fw',
    # 'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr',
    #                              'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],
    # 'STATIC_VIDEOS_EXTENSIONS': ['mp4', 'webm', 'flv', 'mov', 'ogv' ,'3gp' ,'3g2' ,'wmv' ,
    #                              'mpeg' ,'flv' ,'mkv' ,'avi'],

}
# for aws s3
# AWS_S3_ACCESS_KEY_ID
# AWS_S3_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME
# AWS_QUERYSTRING_AUTH

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

STRIPE_PUBLIC_KEY=""
STRIPE_SECRET_KEY=""
STRIPE_WEBHOOK_SECRET=""
