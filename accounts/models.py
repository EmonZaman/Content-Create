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
def upload_and_rename(self, filename):
    ext = filename.split('.')[-1]
    filename = f"{self.team.title}/{self.name.replace(' ', '-')}.{ext}"
    filename = f"resume/employees{filename}" if ext == 'pdf' or ext == 'doc' or ext == 'docs' or ext == 'odt' \
        else f"profile-pics/{filename}"
    return filename


class User(AbstractUser):
    country = models.CharField(max_length=20, null=True, verbose_name=_('user country name'), blank=True)
    profile_pic = models.ImageField(upload_to="media/", verbose_name=_('user profile pic'), blank=True,
                                    null=True)
    secondary_email = models.EmailField(max_length=255,  verbose_name=_('user secondary  email'), unique=True,
                                        blank=True, null=True)
    phone = models.CharField(max_length=255,null=True, verbose_name=_('User phone no'), blank=True)
    content_choice = models.TextField(verbose_name=_("User content-choices"), blank=True)
    gender = models.CharField(max_length=255, null=True, verbose_name=_('User gender'), blank=True)
    facebook = models.CharField(max_length=255, null=True,verbose_name=_('User facebook_link'), blank=True)
    linked_in = models.CharField(max_length=255,null=True, verbose_name=_('User linked in link'), blank=True)

    full_name = models.TextField(blank=True,null=True, verbose_name=_('User full name'))
    age = models.IntegerField(verbose_name=_('user age'),null=True,blank=True)
    language = models.CharField(max_length=255, null=True,verbose_name=_('User language'), blank=True)
    is_pro = models.BooleanField(default=False, verbose_name=_('User is pro or not'))
    pro_expiry_date = models.DateTimeField(null=True, verbose_name=_('Subscription expiry date'), blank=True)
    def get_full_name(self):
        return super().get_full_name()

    def get_google_profile_data(self):
        social_account = SocialAccount.objects.filter(user=self).first()
        try:
            return social_account.extra_data
        except (AttributeError, Exception):
            return {}

