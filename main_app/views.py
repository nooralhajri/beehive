from django.shortcuts import render, redirect
from .models import Channel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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