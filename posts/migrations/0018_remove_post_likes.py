# Generated by Django 5.1.5 on 2025-02-27 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_alter_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
