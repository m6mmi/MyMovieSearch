from django.urls import path
from watchlist.views import WatchlistView, AddToWatchlistView, RemoveFromWatchlistView

app_name = 'watchlist'
urlpatterns = [
    path('<str:username>', WatchlistView.as_view(), name='watchlist'),
    path('<str:username>/add_to_watchlist/', AddToWatchlistView.as_view(), name='add_to_watchlist'),
    # path('watchlist/remove_from_watchlist/', RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
    path('remove_from_watchlist/<int:movie_id>/', RemoveFromWatchlistView.as_view(), name='remove_from_watchlist'),
]
