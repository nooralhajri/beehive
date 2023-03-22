import django
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator



class Channel(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=250, default="")
    profilephoto = models.ImageField(upload_to='main_app/static/uploads/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='channel')

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    thumbnail = models.ImageField(upload_to='main_app/static/uploads/', default='')
    video = models.FileField(upload_to='main_app/static/uploads/', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.id})
    
    def __str__(self):
        return self.title
    


class Subscriber(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='subscribers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('channel', 'user')


class Comment(models.Model):
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    content = models.TextField(max_length=500)


    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.video.id})
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'


class Search(models.Model):
    search = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searches')


