from django.utils.translation import gettext as _
from django.db import models

# Create your models here.
from core.models import BaseModel


class Subscriber(BaseModel):
    first_name = models.CharField(max_length=255, null=True, verbose_name=_('Subscriber first name'), blank=True)
    middle_name = models.CharField(max_length=255, null=True, verbose_name=_('Subscriber middle name'), blank=True)
    last_name = models.CharField(max_length=255, null=True, verbose_name=_('Subscriber last name'), blank=True)
    full_name = models.TextField(blank=True, null=True, verbose_name=_('Subscriber full name'))
    age = models.IntegerField(verbose_name=_('Subscriber age'), null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, verbose_name=_('Subscriber telephone no'), blank=True)
    country = models.CharField(max_length=20, null=True, verbose_name=_('Subscriber country name'), blank=True)
    secondary_email = models.EmailField(max_length=255, verbose_name=_('Subscriber secondary  email'), unique=True,
                                        blank=True, null=True)
    comments = models.TextField(blank=True, null=True, verbose_name=_('Subscriber comments'))

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')

    def __str__(self):
        print(self.first_name)
        return f"{self.first_name}"
