from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Channel(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=250, default="")
    profilephoto = models.ImageField(upload_to='main_app/static/uploads/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    thumbnail = models.ImageField(upload_to='main_app/static/uploads/', default='')
    video = models.FileField(upload_to='main_app/static/uploads/', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.id})



class Subscriber(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default="")

    class Meta:
        unique_together = ('channel', 'user')


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default="")
    timestamp = models.DateTimeField(auto_now_add=True) # This ensures the timestamp is added automatically when the comment is created
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'
    


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

