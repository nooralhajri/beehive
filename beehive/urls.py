from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', include('main_app.urls')),

    path('accounts/change_password/', include('main_app.urls')),
    path('accounts/change_password_done/', include('main_app.urls')),

    path('accounts/password_reset/', include('main_app.urls')),
    path('accounts/password_reset_done/', include('main_app.urls')),
    path('accounts/password_reset_confirm/', include('main_app.urls')),
    path('accounts/password_reset_complete/', include('main_app.urls')),
]


