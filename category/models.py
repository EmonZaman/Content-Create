from django.db import models
from django.utils.translation import gettext as _
from cloudinary.models import CloudinaryField

# Create your models here.
from accounts.models import User
from core.models import BaseModel


def video_upload(self, filename):
    ext = filename.split('.')[-1]
    filename = f"{self.category.name}/{self.title.replace(' ', '-')}.{ext}"
    filename = f"category/videos/{filename}"
    return filename


class Category(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_('category name'))
    description = models.TextField(blank=True, verbose_name=_('category description'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f"{self.name}"


class Video(BaseModel):
    category = models.ForeignKey(Category, verbose_name=_('video category'), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200,blank=True, null=True, verbose_name=_('video title'))
    description = models.TextField(blank=True, null=True,verbose_name=_('video description'))
    video_upload_media = models.FileField(upload_to="media/", verbose_name=_('video upload media'), null=True, blank=True)
    youtube_video_link= models.URLField(max_length=200,verbose_name=_('Youtube video link'), null=True, blank=True)
    video_oid = models.CharField(max_length=200,blank=True, null=True, verbose_name=_('Video oid'))


    # file = CloudinaryField("Video",
    #                        overwrite=True,
    #                        resource_type="video",
    #                        transformation={"quality": "auto:eco"},
    #                        )

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return f"{self.category.name}"


class UserSubscription(BaseModel):
    user = models.OneToOneField(User, verbose_name=_('Auth User'), on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False, verbose_name=_('User is pro or not'))
    pro_expiry_date = models.DateTimeField(null=True, verbose_name=_('Subscription expiry date'), blank=True)
    price = models.IntegerField(verbose_name=_('Subscription price'), null=True, blank=True)

    class Meta:
        verbose_name = _('UserSubscription')
        verbose_name_plural = _('UserSubscriptions')

    def __str__(self):
        print(self.user)
        return f"{self.user.username}"
