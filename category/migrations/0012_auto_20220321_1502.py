# Generated by Django 3.2.9 on 2022-03-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0011_auto_20220320_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='upload',
            new_name='video_upload_media',
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Subscription price'),
        ),
        migrations.AddField(
            model_name='video',
            name='youtube_video_link',
            field=models.URLField(blank=True, null=True, verbose_name='video upload'),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='is_pro',
            field=models.BooleanField(default=False, verbose_name='User is pro or not'),
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='pro_expiry_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Subscription expiry date'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='video description'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='video title'),
        ),
    ]
