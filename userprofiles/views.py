from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from accounts.models import User
from userprofiles.forms import CustomUserChangeForm
from userprofiles.models import UserProfile


class UserDetailsView(UserPassesTestMixin, TemplateView):
    template_name = 'userprofiles/user_profile.html'

    def test_func(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        return self.request.user == user

    def handle_no_permission(self):
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context['user'] = user
        context['user_profile'] = user_profile

        return context


class EditProfileView(UserPassesTestMixin, View):
    form_class = CustomUserChangeForm
    template_name = 'userprofiles/edit_profile.html'

    def test_func(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        return self.request.user == user

    def handle_no_permission(self):
        return redirect('index')

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofiles:profile', username=user.username)
        return render(request, self.template_name, {'form': form})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofiles/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        context['user_profile'] = user_profile

        return context


@method_decorator(login_required, name='dispatch')
class AddToFavoritesView(View):
    print('AddToFavoritesView')
    def post(self, request, *args, **kwargs):
        movie_id = request.POST.get('movie_id')
        title = request.POST.get('title')
        poster_image = request.POST.get('poster_image')

        if not movie_id:
            return redirect('index')

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        favorite_movies = user_profile.favorite_movies

        if user_profile.is_movie_in_watchlist(movie_id):
            favorite_movies = [movie for movie in favorite_movies if movie['movie_id'] != movie_id]
        else:
            favorite_movies.append({'movie_id': movie_id, 'title': title, 'poster_image': poster_image})

        user_profile.favorite_movies = favorite_movies
        user_profile.save()

        return redirect('moviedetails:movie_details', movie_id=movie_id)
