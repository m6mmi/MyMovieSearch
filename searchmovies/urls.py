from django.urls import path

from .views import SearchResultsView

app_name = 'searchmovies'
urlpatterns = [
    path('movie/', SearchResultsView.as_view(), name='search_results'),
]
