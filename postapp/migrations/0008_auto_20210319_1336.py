# Generated by Django 3.1.7 on 2021-03-19 08:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postapp', '0007_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
