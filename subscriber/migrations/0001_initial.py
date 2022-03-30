# Generated by Django 3.2.9 on 2022-03-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subscriber first name')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subscriber middle name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subscriber last name')),
                ('full_name', models.TextField(blank=True, null=True, verbose_name='Subscriber full name')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Subscriber age')),
                ('telephone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subscriber telephone no')),
                ('country', models.CharField(blank=True, max_length=20, null=True, verbose_name='Subscriber country name')),
                ('secondary_email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Subscriber secondary  email')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Subscriber comments')),
            ],
            options={
                'verbose_name': 'Subscriber',
                'verbose_name_plural': 'Subscribers',
            },
        ),
    ]
