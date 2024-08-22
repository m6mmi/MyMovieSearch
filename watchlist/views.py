from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from .models import WatchList


# Create your views here.
class WatchlistView(ListView):
    model = WatchList
    template_name = 'watchlist/watchlist.html'
    context_object_name = 'watchlist'

    def get_queryset(self):
        return WatchList.objects.filter(user_id=self.request.user.id)



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
            movie.save()

        movie.user_id.add(user_id)

        return redirect('watchlist:watchlist', username=request.user.username)