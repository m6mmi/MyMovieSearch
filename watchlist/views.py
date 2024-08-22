from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import WatchList


# Create your views here.
class WatchlistView(ListView):
    model = WatchList
    template_name = 'watchlist/watchlist.html'
    context_object_name = 'watchlist'
    context_profile_picture = 'profile_picture'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WatchlistView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        context['profile_picture'] = user.userprofile.profile_picture
        context['user'] = user
        return context

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username__iexact=username)
        return WatchList.objects.filter(user_id=user.id)



class AddToWatchlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        movie_id = request.POST.get('movie_id')
        title = request.POST.get('title')
        poster_image = request.POST.get('poster_image')
        user_id = request.user.id

        # Check if the movie already exists in the WatchList model
        movie, created = WatchList.objects.get_or_create(movie_id=movie_id,
                                                         defaults={'title': title, 'poster_image': poster_image})
        # If the movie already exists, add the user to the movie
        if created:
            print('Movie created')
            movie.user_id.add(user_id)
        else:
            if movie.user_id.filter(id=user_id).exists():
                # If the user is in the list, remove the user
                print('User removed')
                movie.user_id.remove(user_id)
                if not movie.user_id.exists():
                    # If there are no users in the list, delete the movie
                    print('Movie deleted')
                    movie.delete()
            else:
                print('User added')
                movie.user_id.add(user_id)

        return redirect('moviedetails:movie_details', movie_id=movie_id)