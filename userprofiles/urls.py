from django.urls import path

from .views import UserDetailsView, EditProfileView, BookmarkView, AddToBookmarkView

app_name = 'userprofiles'
urlpatterns = [
    path('<str:username>/', UserDetailsView.as_view(), name='profile'),
    path('<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('<str:username>/bookmarks/', BookmarkView.as_view(), name='bookmarks'),
    path('<str:username>/add_to_favorites/', AddToBookmarkView.as_view(), name='add_to_favorites'),
]