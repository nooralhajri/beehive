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

    path('channels/', views.ChannelList.as_view(), name='channels_index'),
    path('channels/<int:pk>', views.ChannelDetail.as_view(), name='channels_detail'),
    path('channels/create', views.ChannelCreate.as_view(), name='channels_create'),
    path('channels/update/<int:pk>', views.ChannelUpdate.as_view(), name='channels_update'),
    path('channels/delete/<int:pk>', views.ChannelDelete.as_view(), name='channels_delete'),

    #change password 
    path('accounts/change_password/', views.change_password, name='change_password'),
    path('accounts/change_password_done/', views.change_password_done, name='change_password_done'),
]