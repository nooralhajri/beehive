from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .models import Channel, Video, Subscriber, Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateChannelForm, CreateVideoForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponseForbidden

# from .forms import VideoForm


# Create your views here.

def home(request):
    videos = Video.objects.all()
    return render(request, 'home.html', {'videos':videos})

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
    form_class = CreateVideoForm
    # fields = ['title', 'description', 'thumbnail', 'video', 'channel']

    

class VideoDetail(FormMixin, DetailView):
    model = Video
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Subscription status
        channel = self.object.channel
        is_subscribed = False
        if self.request.user.is_authenticated:
            is_subscribed = Subscriber.objects.filter(channel=channel, user=self.request.user).exists()
        context['is_subscribed'] = is_subscribed

        # Comments
        context['comments'] = Comment.objects.filter(video=self.object)

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.video = self.get_object()
        form.save()
        return HttpResponseRedirect(self.request.path)

    

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
    form_class = CreateChannelForm
    # fields = '__all__'
    success_url = '/channels/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


def channels_detail(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscriber.objects.filter(channel=channel, user=request.user).exists()
    return render(request, 'channels/detail.html', {
        'channel': channel,
        'is_subscribed': is_subscribed,
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

#to handle the deletion of comments   
class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('videos_detail', kwargs={'pk': self.object.video.id})

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(user=self.request.user)


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
    
