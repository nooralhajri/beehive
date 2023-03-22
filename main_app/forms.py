from django import forms
from .models import Channel, Video, Comment, User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


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
            'title': forms.TextInput(attrs={'class': 'form-floating form-control bg-primary mb-3  form-text2', 'style':'border-radius: 4rem;' }), 
            'description': forms.Textarea(attrs={'class': 'form-floating form-control bg-primary mb-3' , 'style':'border-radius: 2rem;' }), 
            'video': forms.FileInput(attrs={'class': 'form-floating form-control bg-primary mb-3', 'style':'border-radius: 4rem;' }), 
            'thumbnail': forms.FileInput(attrs={'class': 'form-floating form-control bg-primary mb-3', 'style':'border-radius: 4rem;' }), 
            'channel': forms.Select(attrs={'class': 'form-select form-control bg-primary mb-3', 'style':'border-radius: 4rem;' }),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control bg-primary mb-3'}),
        }


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control bg-primary text-light ::-webkit-input-placeholder',
        'style': 'border-radius: 4rem; color:white; color: white;::placeholder {color: white;}',
        'placeholder' : 'hello@beehive.com'
        }))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class':'form-control bg-primary text-light',
        'style': 'border-radius: 4rem;',
        'placeholder' : 'Bee'
        }))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class':'form-control bg-primary text-light',
        'style': 'border-radius: 4rem;',
        'placeholder' : 'Hive',
        }))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control bg-primary text-light',
            'style': 'border-radius: 4rem; color: white;'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control bg-primary text-light',
            'style': 'border-radius: 4rem; color: white;'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control bg-primary text-light',
            'style': 'border-radius: 4rem; color: white;'
        })


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control bg-primary text-light',
                'style': 'border-radius: 4rem; color: white;'
            })


