from django.shortcuts import render
from .models import Channel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

def home(request):
    return render(request, 'home.html')
