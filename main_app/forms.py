from django import forms
from .models import Channel, Tag, Video, Comment

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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Video
        fields = ['title', 'description', 'video', 'thumbnail', 'channel', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'description': forms.Textarea(attrs={'class': 'form-control'}), 
            'video': forms.FileInput(attrs={'class': 'form-control'}), 
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}), 
            'channel': forms.Select(attrs={'class': 'form-control'}), 
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
