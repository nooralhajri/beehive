from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    joindate = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)

    #foreign key of the user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

