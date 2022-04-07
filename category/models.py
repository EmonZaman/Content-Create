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
    category_thumbnail = models.ImageField(upload_to="media/", verbose_name=_('category thumbnail'), blank=True,
                                           null=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f"{self.name}"


class Video(BaseModel):
    category = models.ForeignKey(Category, verbose_name=_('video category'), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('video title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('video description'))
    video_upload_media = models.FileField(upload_to="media/", verbose_name=_('video upload media'), null=True,
                                          blank=True)
    videos_thumbnail = models.FileField(upload_to="media/", verbose_name=_('videos thumbnail'), blank=True,
                                         null=True)
    youtube_video_link = models.URLField(max_length=200, verbose_name=_('Youtube video link'), null=True, blank=True)
    video_oid = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Video oid'))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __str__(self):
        return f"{self.id} {self.title}"


class VideoLikes(models.Model):
    likeusers = models.ManyToManyField(User, null=True, blank=True, verbose_name=_('liked user id list'))
    likevideo = models.OneToOneField(Video, null=True, on_delete=models.CASCADE, verbose_name=_('video id'))

    class Meta:
        verbose_name = _('VideoLike')
        verbose_name_plural = _('VideoLikes')

    # def __str__(self):
    #     return f"{self.likevideo.id}"


class SaveVideos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user id'))
    video = models.ManyToManyField(Video
                                   ,null=True,blank=True, verbose_name=_('saved videos id list'))

    class Meta:
        verbose_name = _('SaveVideo')
        verbose_name_plural = _('SaveVideos')

    def __str__(self):
        return f"{self.user.username}"


class RecentShownVideos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user id'))
    video = models.ManyToManyField(Video
                                   ,null=True, blank=True, verbose_name=_('saved videos id list'))

    class Meta:
        verbose_name = _('RecentShownVideo')
        verbose_name_plural = _('RecentShownVideos')

    def __str__(self):
        return f"{self.user.username}"


class UserSubscription(BaseModel):
    user = models.OneToOneField(User, verbose_name=_('Auth User'), on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True, verbose_name=_('Subscription name'))
    is_pro = models.BooleanField(default=False, verbose_name=_('User is pro or not'))
    pro_expiry_date = models.DateTimeField(null=True, verbose_name=_('Subscription expiry date'), blank=True)
    price = models.IntegerField(verbose_name=_('Subscription price'), default=0)

    class Meta:
        verbose_name = _('UserSubscription')
        verbose_name_plural = _('UserSubscriptions')

    def __str__(self):
        print(self.user)
        return f"{self.user.username}"

    def get_display_price(self):
        return "{0:.2f}".format((self.price / 100))
