from django.shortcuts import render, redirect
from .models import Channel, Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView


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
            return redirect('home')
        else:
            error_message = 'hey stupid try Again'
    form = UserCreationForm()
    context = {'form': form, 'error_massage': error_message}
    return render(request, 'registration/signup.html', context)



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



