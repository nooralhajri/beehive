# Generated by Django 4.1.7 on 2023-03-20 12:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_tag_remove_channel_video_video_channel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
