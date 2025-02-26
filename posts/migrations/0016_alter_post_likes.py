# Generated by Django 5.1.5 on 2025-02-27 06:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_post_likes_postlikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(through='posts.PostLikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
