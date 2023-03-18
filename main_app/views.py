from django.shortcuts import render, redirect
from .models import Channel, Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')


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
