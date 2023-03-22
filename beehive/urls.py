from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #change password 
    path('change-password/',
          auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url = '/'

            ),
             name='change_password'),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password_reset_form.html',
             subject_template_name='commons/password_reset_subject.txt',
             email_template_name='commons/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    #email verification
        path('password_reset_email/', auth_views.PasswordResetView.as_view(
            email_template_name='commons/password_reset_email.html',
            html_email_template_name='commons/password_reset_email_html.html',
            subject_template_name='commons/password_reset_subject.txt',
            extra_email_context={'email_host_user': settings.EMAIL_HOST_USER}
        ), name='password_reset_email'),

]