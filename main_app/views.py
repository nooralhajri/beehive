from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .models import Channel, Video, Subscriber, Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateChannelForm, CreateVideoForm, RegisterUserForm, CommentForm, ChangePasswordForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Home view  
def home(request):
    search_query = request.GET.get('q')
    if search_query:
        return redirect('search_results', search_query=search_query)
    else:
        video_list = Video.objects.all()
        paginator = Paginator(video_list, 12)
        page = request.GET.get('page')
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'videos': videos})
    
    

# Sign up function
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = RegisterUserForm()
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
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})


# Video class-based views
class VideoList(ListView):
    model = Video
    template_name = 'video_list.html'
    paginate_by = 12  # Show 12 videos per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_list = Video.objects.all()
        paginator = Paginator(video_list, 12)
        page = self.request.GET.get('page')
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)
        context['page_obj'] = videos
        return context

class VideoCreate(CreateView):
    model = Video
    form_class = CreateVideoForm

class VideoDetail(DetailView):
    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.object
        # to retrieve all comments associated with the current video
        comments = Comment.objects.filter(video=video)
        context['comments'] = comments
        context['form'] = CommentForm()
        return context
    
class VideoUpdate(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = CreateVideoForm


class VideoDelete(LoginRequiredMixin, DeleteView):
    model = Video

    def get_success_url(self):
        return reverse('home')


# CHANNEL CLASS BASED VIEWS
def channels_index(request):
    channels = Channel.objects.all()
    return render(request, 'channels/index.html', {'channels': channels})

def channels_detail(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscriber.objects.filter(channel=channel, user=request.user).exists()
    return render(request, 'channels/detail.html', {
        'channel': channel,
        'is_subscribed': is_subscribed,
    }) 

class ChannelCreate(CreateView):
    model = Channel
    form_class = CreateChannelForm
    # fields = '__all__'
    success_url = '/channels/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
    


class ChannelUpdate(UpdateView):
    model = Channel
    fields = '__all__'
    
    
class ChannelDelete(DeleteView):
    model = Channel
    success_url = '/channels/'

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
    template_name = 'commons/password_reset_form.html'
    email_template_name = 'commons/password_reset_email.html'
    subject_template_name = 'commons/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'commons/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'commons/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'commons/password_reset_complete.html'

# Add Comment Views
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'main_app/comment_form.html'

    def form_valid(self, form):
        form.instance.video_id = self.kwargs['video_id']
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('videos_detail', kwargs={'pk': self.object.video.pk})

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('videos_detail', kwargs={'pk': self.object.video.id})


# Add Subscriber Views
@login_required
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

# Search Views

def search_results(request):
    query = request.GET.get('q')
    videos = Video.search(query)
    paginator = Paginator(videos, 10)
    page = request.GET.get('page')
    videos = paginator.get_page(page)
    return render(request, 'search_results.html', {'videos': videos, 'query': query})

# ADDING PAGINATION
def my_view(request):
    # Query all objects
    videos = Video.objects.all()

    # Create a Paginator object with 10 objects per page
    paginator = Paginator(videos, 12)

    # Get the current page number
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj})

