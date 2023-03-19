from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    thumbnail = models.ImageField(upload_to='main_app/static/uploads/', default='')
    video = models.FileField(upload_to='main_app/static/uploads/', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.id})
    

class Channel(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=250, default="")
    profilephoto = models.ImageField(upload_to='main_app/static/uploads/', blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)


