from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .models import Channel, Video, Subscriber, Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

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
    fields = ['title', 'description', 'thumbnail', 'video', 'channel']
    
    
class VideoDetail(DetailView):
    model = Video


class VideoUpdate(UpdateView):
    model = Video
    fields = '__all__'
    
    
class VideoDelete(DeleteView):
    model = Video
    success_url = '/'


# CHANNEL CLASS BASED VIEWS
def channels_index(request):
    channels = Channel.objects.all()
    return render(request, 'channels/index.html', {'channels': channels})

    

class ChannelCreate(CreateView):
    model = Channel
    fields = '__all__'
    success_url = '/channels/'
    
    
def channels_detail(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    return render(request, 'channels/detail.html', {
        'channel': channel,
        })


class ChannelUpdate(UpdateView):
    model = Channel
    fields = '__all__'
    
    
class ChannelDelete(DeleteView):
    model = Channel
    success_url = '/channels/'

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



# Add Comment Views
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'main_app/comment_form.html'

    def form_valid(self, form):
        form.instance.video_id = self.kwargs['video_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

# Add Subscriber Views
class SubscriberCreate(LoginRequiredMixin, CreateView):
    model = Subscriber
    fields = []

    def form_valid(self, form):
        form.instance.channel_id = self.kwargs['channel_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

class SubscriberDelete(LoginRequiredMixin, DeleteView):
    model = Subscriber
    success_url = '/channels/'

    def get_object(self):
        channel_id = self.kwargs['channel_pk']
        user = self.request.user
        return Subscriber.objects.get(channel_id=channel_id, user=user)
    
