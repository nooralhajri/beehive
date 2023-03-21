from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),

    path('videos/', views.VideoList.as_view(), name='videos_index'),
    path('videos/<int:pk>', views.comments, name='videos_detail'),
    path('videos/create', views.VideoCreate.as_view(), name='videos_create'),
    path('videos/update/<int:pk>', views.VideoUpdate.as_view(), name='videos_update'),
    path('videos/delete/<int:pk>', views.VideoDelete.as_view(), name='videos_delete'),

    path('channels/', views.channels_index, name='index'),
    path('channels/<int:channel_id>/', views.channels_detail, name='detail'),
    path('channels/create', views.ChannelCreate.as_view(), name='channels_create'),
    path('channels/update/<int:pk>', views.ChannelUpdate.as_view(), name='channels_update'),
    path('channels/delete/<int:pk>', views.ChannelDelete.as_view(), name='channels_delete'),

    #change password 
    path('accounts/change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'), name='change_password'),
    path('accounts/change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='password_change_done'),

    #reset password
    path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset_email/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_email'),
    path('accounts/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #email verification
    path('accounts/password_reset_email/', auth_views.PasswordResetView.as_view(
        email_template_name='registration/password_reset_email.html',
        html_email_template_name='registration/password_reset_email_html.html',
        subject_template_name='registration/password_reset_subject.txt',
        extra_email_context={'email_host_user': settings.EMAIL_HOST_USER}
    ), name='password_reset_email'),

    # Comment URLs
    path('videos/<int:video_pk>', views.CommentCreate.as_view(), name='comment_create'),

    # Subscriber URLs
    path('channels/<int:channel_id>/subscribe/', views.subscribe, name='subscribe'),

    # Search URL
    path('search/', views.search_results, name='search_results'),

    #pagination url
    path('videos/page/<int:page>/', views.VideoList.as_view(), name='videos_index'),
]
