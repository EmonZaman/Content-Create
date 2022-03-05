from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.

class User(AbstractUser):
    country = models.CharField(max_length=20, verbose_name=_('user country name'), blank=True)


    def get_full_name(self):
        return super().get_full_name()

    def get_google_profile_data(self):
        social_account = SocialAccount.objects.filter(user=self).first()
        try:
            return social_account.extra_data
        except (AttributeError, Exception):
            return {}

