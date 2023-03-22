from django import forms
from .models import Channel, Video, Comment

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
 
        fields = ['title', 'description', 'video', 'thumbnail', 'channel']


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-floating form-control bg-primary mb-3  form-text2' }), 
            'description': forms.Textarea(attrs={'class': 'form-floating form-control bg-primary mb-3 ' }), 
            'video': forms.FileInput(attrs={'class': 'form-floating form-control bg-primary mb-3 ' }), 
            'thumbnail': forms.FileInput(attrs={'class': 'form-floating form-control bg-primary mb-3 ' }), 
            'channel': forms.Select(attrs={'class': 'form-select form-control bg-primary mb-3 ' }),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control bg-primary mb-3 ' }), 
        }

