from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .models import Channel, Dislike, Like, Playlist, Tag, Video, Subscriber, Comment, PlaylistVideo
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateChannelForm, CreateVideoForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse

# Home view
def home(request):
    videos = Video.objects.all()
    return render(request, 'home.html', {'videos': videos})

# Sign up function
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# View for the user's profile
@login_required
def profile(request):
    user = request.user
    videos = Video.objects.filter(user=user)
    return render(request, 'profile.html', {'user': user, 'videos': videos})

# Change password
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

# Video class-based views
class VideoList(ListView):
    model = Video

class VideoCreate(LoginRequiredMixin, CreateView):
    model = Video
    form_class = CreateVideoForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

class VideoUpdate(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = CreateVideoForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class VideoDelete(LoginRequiredMixin, DeleteView):
    model = Video

    def get_success_url(self):
        return reverse('home')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Video.objects.all()
        return Video.objects.filter(user=self.request.user)

# CHANNEL CLASS BASED VIEWS
def channels_index(request):
    channels = Channel.objects.all()
    return render(request, 'channels/index.html', {'channels': channels})

class ChannelCreate(LoginRequiredMixin, CreateView):
    model = Channel
    form_class = CreateChannelForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('channels_detail', kwargs={'pk': self.object.id})

class ChannelDetail(LoginRequiredMixin, DetailView):
    model = Channel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel = self.object
        is_subscribed = False
        if self.request.user.is_authenticated:
            is_subscribed = Subscriber.objects.filter(channel=channel, user=self.request.user).exists()
        context['is_subscribed'] = is_subscribed
        return context
    
    

class ChannelUpdate(LoginRequiredMixin, UpdateView):
    model = Channel
    form_class = CreateChannelForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChannelDelete(LoginRequiredMixin, DeleteView):
    model = Channel

    def get_success_url(self):
        return reverse('channels_index')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Channel.objects.all()
        return Channel.objects.filter(user=self.request.user)

@login_required
def subscribe(request, channel_id):
    if request.method == 'POST':
        channel = get_object_or_404(Channel, pk=channel_id)
        user = request.user
        subscribe = request.POST.get('subscribe', 'false') == 'true'

        if subscribe:
            channel.subscribers.add(user)
            new_subscription_count = channel.subscribers.count()
            return JsonResponse({'status': 'success', 'new_subscription_count': new_subscription_count})
        else:
            channel.subscribers.remove(user)
            new_subscription_count = channel.subscribers.count()
            return JsonResponse({'status': 'success', 'new_subscription_count': new_subscription_count})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

# Add Comment Views
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'main_app/comment_form.html'

    def form_valid(self, form):
        form.instance.video_id = self.kwargs['video_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

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
        response_data = {}

        try:
            # Save the subscription.
            self.object = form.save()
            # Update the subscription count for the user.
            new_subscription_count = self.request.user.subscriptions.count()
            response_data = {
                "status": "success",
                "new_subscription_count": new_subscription_count
            }
        except ValidationError as e:
            response_data = {"status": "error", "message": str(e)}

        return JsonResponse(response_data)

# Add Like Views
class LikeCreate(LoginRequiredMixin, CreateView):
    model = Like
    fields = []

    def form_valid(self, form):
        form.instance.video_id = self.kwargs['video_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

class LikeDelete(LoginRequiredMixin, DeleteView):
    model = Like
    success_url = '/videos/'

    def get_object(self):
        video_id = self.kwargs['video_pk']
        user = self.request.user
        return Like.objects.get(video_id=video_id, user=user)

# Add Dislike Views
class DislikeCreate(LoginRequiredMixin, CreateView):
    model = Dislike
    fields = []

    def form_valid(self, form):
        form.instance.video_id = self.kwargs['video_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

class DislikeDelete(LoginRequiredMixin, DeleteView):
    model = Dislike
    success_url = '/videos/'

    def get_object(self):
        video_id = self.kwargs['video_pk']
        user = self.request.user
        return Dislike.objects.get(video_id=video_id, user=user)

# Add Playlist Views
class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlaylistUpdate(LoginRequiredMixin, UpdateView):
    model = Playlist
    fields = ['name']

class PlaylistDelete(LoginRequiredMixin, DeleteView):
    model = Playlist
    success_url = '/playlists/'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Playlist.objects.all()
        return Playlist.objects.filter(user=self.request.user)

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist

class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

class PlaylistVideoCreate(LoginRequiredMixin, CreateView):
    model = PlaylistVideo
    fields = ['video']

    def form_valid(self, form):
        form.instance.playlist_id = self.kwargs['playlist_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlaylistVideoDelete(LoginRequiredMixin, DeleteView):
    model = PlaylistVideo

    def get_success_url(self):
        return reverse('playlists_detail', kwargs={'pk': self.object.playlist.id})

    def get_queryset(self):
        if self.request.user.is_staff:
            return PlaylistVideo.objects.all()
        return PlaylistVideo.objects.filter(user=self.request.user)

class TagList(LoginRequiredMixin, ListView):
    model = Tag

class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag

class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name']

class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name']

class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tags_index')

def search(request):
    query = request.GET.get('q')

    if query:
        videos = Video.objects.filter(title__icontains=query)
    else:
        videos = Video.objects.all()

    return render(request, 'search.html', {'videos': videos})
