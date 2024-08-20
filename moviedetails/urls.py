from django.urls import path

from .views import MovieDetailsView

app_name = 'moviedetails'
urlpatterns = [
    path('<int:movie_id>/', MovieDetailsView.as_view(), name='movie_details'),
]