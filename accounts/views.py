# accounts/views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
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
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            return redirect(reverse_lazy('userprofiles:profile', kwargs={'username': self.request.user.username}))
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('userprofiles:profile', kwargs={'username': self.request.user.username})
