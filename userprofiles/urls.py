from django.urls import path

from .views import UserDetailsView, EditProfileView, DashboardView, AddToFavoritesView

app_name = 'userprofiles'
urlpatterns = [
    path('<str:username>/', UserDetailsView.as_view(), name='profile'),
    path('<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('<str:username>/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<str:username>/add_to_favorites/', AddToFavoritesView.as_view(), name='add_to_favorites'),
]