from django import forms
from .models import Channel, Video

class CreateChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'about', 'profilephoto']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'about': forms.TextInput(attrs={'class': 'form-control'}), 
            'profilephoto': forms.FileInput(attrs={'class': 'form-control'}), 
        }


class CreateVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video', 'thumbnail']


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'description': forms.Textarea(attrs={'class': 'form-control'}), 
            'video': forms.FileInput(attrs={'class': 'form-control'}), 
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}), 
        }
        

