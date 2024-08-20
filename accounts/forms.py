from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'invalid': 'Enter a valid email address.'}
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        error_messages={'required': 'Username is required.'}
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        error_messages={'required': 'Password is required.'}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        error_messages={'required': 'Please confirm your password.'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user = User.objects.get(username__iexact=username)
                    self.user_cache = authenticate(self.request, username=user.username, password=password)
                except User.DoesNotExist:
                    pass
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
