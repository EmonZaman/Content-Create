# Generated by Django 3.2.9 on 2022-04-06 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220323_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name='user profile pic'),
        ),
    ]