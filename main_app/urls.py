from django.urls import path
from. import views



urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),

    path('videos/', views.VideoList.as_view(), name='videos_index'),
    path('videos/<int:pk>', views.VideoDetail.as_view(), name='videos_detail'),
    path('videos/create', views.VideoCreate.as_view(), name='videos_create'),
    path('videos/update/<int:pk>', views.VideoUpdate.as_view(), name='videos_update'),
    path('videos/delete/<int:pk>', views.VideoDelete.as_view(), name='videos_delete'),

    path('channels/', views.channels_index, name='channels'),
    path('channels/<int:channel_id>', views.channels_detail, name='detail'),
    path('channels/create', views.ChannelCreate.as_view(), name='channels_create'),
    path('channels/update/<int:pk>', views.ChannelUpdate.as_view(), name='channels_update'),
    path('channels/delete/<int:pk>', views.ChannelDelete.as_view(), name='channels_delete'),

    #change password 
    path('accounts/change_password/', views.change_password, name='change_password'),
    path('accounts/change_password_done/', views.change_password_done, name='change_password_done'),

    #reset password
    path('accounts/password_reset/', views.password_reset, name='password_reset'),
    path('accounts/password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('accounts/password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('accounts/password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    
    # Comment URLs
    path('videos/<int:video_pk>/comment/', views.CommentCreate.as_view(), name='comment_create'),
    path('comments/delete/<int:pk>/', views.CommentDelete.as_view(), name='comment_delete'),

    # Subscriber URLs
    path('channels/<int:channel_id>/subscribe/', views.subscribe, name='subscribe'),
    # path('channels/<int:channel_pk>/unsubscribe/', views.SubscriberDelete.as_view(), name='unsubscribe'),

    # Like URLs
    path('videos/<int:video_pk>/like/', views.LikeCreate.as_view(), name='like'),
    path('videos/<int:video_pk>/unlike/', views.LikeDelete.as_view(), name='unlike'),

    # # Search URL
    # path('search/', views.search, name='search'),

    # # profile URL
    # path('profile/', views.profile, name='profile'),
    # path('profile/update/<int:pk>', views.ProfileUpdate.as_view(), name='profile_update'),
    # path('profile/delete/<int:pk>', views.ProfileDelete.as_view(), name='profile_delete'),

]