# Generated by Django 3.2.9 on 2022-03-31 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0017_alter_videolikes_likevideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videolikes',
            name='likevideo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likevideos', to='category.video'),
        ),
    ]
