from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),

    path('videos/', views.VideoList.as_view(), name='videos_index'),
    # path('videos/<int:pk>', views.comments, name='videos_detail'),
    path('videos/<int:pk>/', views.VideoDetail.as_view(), name='videos_detail'),
    path('videos/create', views.VideoCreate.as_view(), name='videos_create'),
    path('videos/update/<int:pk>', views.VideoUpdate.as_view(), name='videos_update'),
    path('videos/delete/<int:pk>', views.VideoDelete.as_view(), name='videos_delete'),

    path('channels/', views.channels_index, name='index'),
    path('channels/<int:channel_id>/', views.channels_detail, name='detail'),
    path('channels/create', views.ChannelCreate.as_view(), name='channels_create'),
    path('channels/update/<int:pk>', views.ChannelUpdate.as_view(), name='channels_update'),
    path('channels/delete/<int:pk>', views.ChannelDelete.as_view(), name='channels_delete'),


    # Comment URLs
    path('videos/<int:video_id>/comment/', views.CommentCreate.as_view(), name='comment_create'),

    # Subscriber URLs
    path('channels/<int:channel_id>/subscribe/', views.subscribe, name='subscribe'),

    # Search URL
    path('search/', views.search_results, name='search_results'),

    #pagination url
    path('videos/page/<int:page>/', views.VideoList.as_view(), name='videos_index'),
]