from django.views.generic import TemplateView

from moviedetails.utils import details_movie, cast_list
from userprofiles.models import UserProfile
from watchlist.models import WatchList


# Create your views here.
class MovieDetailsView(TemplateView):
    template_name = 'moviedetails/movie_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('movie_id')
        details = details_movie(movie_id)
        casts = cast_list(movie_id)

        if self.request.user.is_authenticated:
            user_movies = UserProfile.objects.get(user=self.request.user)
            is_in_bookmarks = user_movies.is_movie_in_bookmarks(movie_id)
            is_in_watchlist = WatchList.is_movie_in_watchlist(movie_id_from_view=movie_id, user=self.request.user)

            if is_in_bookmarks:
                watchlist_button_text = 'Remove from Bookmarks'
                context['bookmark_button_text'] = watchlist_button_text
            else:
                watchlist_button_text = 'Add to Bookmarks'
                context['bookmark_button_text'] = watchlist_button_text

            if is_in_watchlist:
                watchlist_button_text = 'Remove from Watchlist'
                context['watchlist_button_text'] = watchlist_button_text
            else:
                watchlist_button_text = 'Add to Watchlist'
                context['watchlist_button_text'] = watchlist_button_text

        context['movie_id'] = movie_id
        context['details'] = details
        context['casts'] = casts

        return context
