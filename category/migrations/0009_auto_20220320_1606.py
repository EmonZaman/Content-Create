# Generated by Django 3.2.9 on 2022-03-20 16:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0008_alter_usersubcription_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubcription',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersubcription',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
