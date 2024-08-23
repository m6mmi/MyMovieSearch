from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from moviedetails.forms import ReviewForm
from moviedetails.models import Review
from moviedetails.utils import details_movie, cast_list
from userprofiles.models import UserProfile
from watchlist.models import WatchList


# Create your views here.
class MovieDetailsView(TemplateView):
    template_name = 'moviedetails/movie_details.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('movie_id')
        details = details_movie(movie_id)
        casts = cast_list(movie_id)
        reviews_list = Review.objects.filter(movie_id=movie_id).order_by('-created_at')
        print(reviews_list.values())


        if self.request.user.is_authenticated:
            user_movies = UserProfile.objects.get(user=self.request.user)
            is_in_bookmarks = user_movies.is_movie_in_bookmarks(movie_id)
            is_in_watchlist = WatchList.is_movie_in_watchlist(movie_id_from_view=movie_id, user=self.request.user)
            context['form'] = self.form_class
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
        context['reviews_list'] = reviews_list

        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.instance.movie_id = self.kwargs.get('movie_id')
            form.comment = form.cleaned_data.get('comment')
            form.rating = form.cleaned_data.get('rating')
    
            form.save()
            return redirect(request.path_info)
        return self.render_to_response(self.get_context_data(form=form))



