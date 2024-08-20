from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, CustomLoginView, ActivateAccountView

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]
