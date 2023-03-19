from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .models import Channel, Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# from .forms import VideoForm


# Create your views here.

def home(request):
    return render(request, 'home.html')

# Sign up function 

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})


@login_required
def change_password_done(request):
    return render(request, 'registration/change_password_done.html')

# reset password
def password_reset(request):
    return render(request, 'registration/password_reset.html')

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')


# VIDEO CLASS BASED VIEWS
class VideoList(ListView):
    model = Video
    

class VideoCreate(CreateView):
    model = Video
    fields = '__all__'
    
    
class VideoDetail(DetailView):
    model = Video


class VideoUpdate(UpdateView):
    model = Video
    fields = '__all__'
    
    
class VideoDelete(DeleteView):
    model = Video
    success_url = '/'


# CHANNEL CLASS BASED VIEWS
class ChannelList(ListView):
    model = Channel
    

class ChannelCreate(CreateView):
    model = Channel
    fields = '__all__'
    
    
class ChannelDetail(DetailView):
    model = Channel


class ChannelUpdate(UpdateView):
    model = Channel
    fields = '__all__'
    
    
class ChannelDelete(DeleteView):
    model = Channel
    success_url = '/'

# Password reset views

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
#     template_name = 'registration/password_reset_complete.html'
# # Adding video to the channel funcion
# def add_video(request, channel_id):
#     form = VideoForm(request.POST)
#     if form.is_valid():
#         new_video = form.save(commit=False)
#         new_video.channel_id = channel_id
#         new_video.save()
#     return redirect('detail', channel_id=channel_id)

