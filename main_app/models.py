from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    thumbnail = models.ImageField(upload_to='images_uploaded', null=True)
    video = models.FileField(upload_to='videos_uploaded', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])


class Channel(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=250, default="")
    profilephoto = models.ImageField(upload_to='images/', blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)


