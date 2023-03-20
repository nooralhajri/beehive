import django
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
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.id})



class Subscriber(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('channel', 'user')


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    # liked_by = models.ManyToManyField(User, blank=True)
    # disliked_by = models.ManyToManyField(User, blank=True)

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.video.id})
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'
    


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})
    
class Search(models.Model):
    search = models.CharField(max_length=100)
    search_date = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.search
    
class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('video', 'user')

class Dislike(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('video', 'user')

class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('comment', 'user')

class DislikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('comment', 'user')

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('playlists_detail', kwargs={'pk': self.id})
    
class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('playlist', 'video')

class History(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('video', 'user')

class WatchLater(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('video', 'user')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('notifications_detail', kwargs={'pk': self.id})

class Report(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.reason

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.video.id})
    
class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.reason

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.comment.video.id})
    
class ReportChannel(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.reason

    def get_absolute_url(self):
        return reverse('channels_detail', kwargs={'pk': self.channel.id})
    

class Subscription(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('channel', 'user')

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.comment.video.id})
    
class CommentReplyLike(models.Model):
    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('comment_reply', 'user')

class CommentReplyDislike(models.Model):
    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = ('comment_reply', 'user')



    


