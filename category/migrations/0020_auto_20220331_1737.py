# Generated by Django 3.2.9 on 2022-03-31 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0019_auto_20220331_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='category thumbnail'),
        ),
        migrations.AddField(
            model_name='video',
            name='videos_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='videos thumbnail'),
        ),
    ]
