from django.contrib import admin
from .models import Video, Channel, Comment, Subscriber, Tag

# Register your models 
admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(Tag)
