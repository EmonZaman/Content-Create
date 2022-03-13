from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
# def upload_and_rename(self, filename):
#     ext = filename.split('.')[-1]
#     filename = f"{self.team.title}/{self.name.replace(' ', '-')}.{ext}"
#     filename = f"resume/employees{filename}" if ext == 'pdf' or ext == 'doc' or ext == 'docs' or ext == 'odt' \
#         else f"profile-pics/{filename}"
#     return filename


class User(AbstractUser):
    country = models.CharField(max_length=20, verbose_name=_('user country name'), blank=True)
    # profile_pic = models.ImageField(upload_to=upload_and_rename, verbose_name=_('user profile pic'), blank=True,
    #                                 null=True)


    def get_full_name(self):
        return super().get_full_name()

    def get_google_profile_data(self):
        social_account = SocialAccount.objects.filter(user=self).first()
        try:
            return social_account.extra_data
        except (AttributeError, Exception):
            return {}

