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
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    tags = models.ManyToManyField('Tag', blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_videos', blank=True)

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.id})
    
    def __str__(self):
        return self.title
    
    @staticmethod
    def search(query):
        return Video.objects.filter(title__icontains=query)


class Subscriber(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='subscribers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('channel', 'user')


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

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
    search_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searches')

    def __str__(self):
        return self.search

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    videos = models.ManyToManyField(Video, blank=True, related_name='playlists')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('playlists_detail', kwargs={'pk': self.id})

class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

  
class History(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='histories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')


class WatchLater(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watchlaters')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlaters')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('notifications_detail', kwargs={'pk': self.id})


class Report(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.reason

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.video.id})


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_replies')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('videos_detail', kwargs={'pk': self.comment.video.id})


class CommentReplyLike(models.Model):
    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reply_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment_reply', 'user')


class CommentReplyDislike(models.Model):
    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reply_dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment_reply', 'user')

class Dislike(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')

class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')