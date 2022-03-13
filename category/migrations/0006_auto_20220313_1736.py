# Generated by Django 3.2.9 on 2022-03-13 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_alter_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='file',
        ),
        migrations.AddField(
            model_name='video',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name='video upload'),
        ),
    ]