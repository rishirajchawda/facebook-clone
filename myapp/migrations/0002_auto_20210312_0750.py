# Generated by Django 3.1.7 on 2021-03-12 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/post_pic'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/post_pic'),
        ),
    ]
