# accounts/views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from userprofiles.models import FavoriteMovie
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            FavoriteMovie.objects.create(user=user)
            activate_email(request, user, form.cleaned_data.get('email'))
            # return redirect(reverse_lazy('index'))
        return render(request, self.template_name, {'form': form})


def activate_email(request, user, email):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse_lazy('accounts:activate', kwargs={'uidb64': uid, 'token': token})
    )
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_link': activation_link
    })
    send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email])
    messages.success(request, f'An email has been sent to {email}. Please confirm to activate your account.')


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('userprofiles:profile', kwargs={'username': self.request.user.username})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been activated successfully!')
            return redirect(reverse_lazy('userprofiles:profile', kwargs={'username': user.username}))
        else:
            messages.error(request, 'The activation link is invalid!')
            return redirect(reverse_lazy('index'))