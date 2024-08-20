# userprofiles/forms.py
import os

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from userprofiles.models import UserProfile

class CustomUserChangeForm(UserChangeForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Bio'}), required=False)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'placeholder': 'placeholder.png'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'birth_date', 'profile_picture')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            user_profile = UserProfile.objects.get(user=self.instance)
            self.fields['bio'].initial = user_profile.bio
            self.fields['birth_date'].initial = user_profile.birth_date
            self.fields['profile_picture'].initial = user_profile.profile_picture

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.bio = self.cleaned_data['bio']
            user_profile.birth_date = self.cleaned_data['birth_date']
            if self.cleaned_data['profile_picture']:
                user_profile.profile_picture = os.path.basename(self.cleaned_data['profile_picture'].name)
            else:
                user_profile.profile_picture = 'placeholder.png'
            user_profile.save()
        return user
