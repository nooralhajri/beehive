from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),

    path('videos/', views.VideoList.as_view(), name='videos_index'),
    path('videos/<int:pk>', views.VideoDetail.as_view(), name='videos_detail'),
    path('videos/create', views.VideoCreate.as_view(), name='videos_create'),
    path('videos/update/<int:pk>', views.VideoUpdate.as_view(), name='videos_update'),
    path('videos/delete/<int:pk>', views.VideoDelete.as_view(), name='videos_delete'),

    path('channels/', views.channels_index, name='channels'),
    path('channels/<int:pk>/', views.ChannelDetail.as_view(), name='channel_detail'),
    path('channels/create', views.ChannelCreate.as_view(), name='channels_create'),
    path('channels/update/<int:pk>', views.ChannelUpdate.as_view(), name='channels_update'),
    path('channels/delete/<int:pk>', views.ChannelDelete.as_view(), name='channels_delete'),

    #change password 
    path('accounts/change_password/', views.change_password, name='change_password'),
    # path('accounts/change_password_done/', views.change_password_done, name='change_password_done'),

    #reset password
    path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Comment URLs
    path('videos/<int:video_pk>/comment/', views.CommentCreate.as_view(), name='comment_create'),
    path('comments/delete/<int:pk>/', views.CommentDelete.as_view(), name='comment_delete'),

    # Subscriber URLs
    path('channels/<int:channel_id>/subscribe/', views.subscribe, name='subscribe'),

    # Search URL
    path('search/', views.search, name='search'),

    # Playlist URLs
    path('playlists/', views.PlaylistListView.as_view(), name='playlists_index'),
    path('playlists/<int:pk>', views.PlaylistDetailView.as_view(), name='playlists_detail'),
    path('playlists/create', views.PlaylistCreate.as_view(), name='playlists_create'),
    path('playlists/update/<int:pk>', views.PlaylistUpdate.as_view(), name='playlists_update'),
    path('playlists/delete/<int:pk>', views.PlaylistDelete.as_view(), name='playlists_delete'),

    # PlaylistVideo URLs
    path('playlists/<int:playlist_pk>/add_video/', views.PlaylistVideoCreate.as_view(), name='playlistvideo_create'),
    path('playlists/<int:playlist_pk>/remove_video/<int:pk>/', views.PlaylistVideoDelete.as_view(), name='playlistvideo_delete'),

    # Tag URL
    path('tags/', views.TagList.as_view(), name='tags_index'),
    path('tags/<int:pk>', views.TagDetail.as_view(), name='tags_detail'),
    path('tags/create', views.TagCreate.as_view(), name='tags_create'),
    path('tags/update/<int:pk>', views.TagUpdate.as_view(), name='tags_update'),
    path('tags/delete/<int:pk>', views.TagDelete.as_view(), name='tags_delete'),

]
