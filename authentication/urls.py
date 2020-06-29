from django.urls import path
from .views import LoginView, RegisterView, UserProfileView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', RegisterView.as_view()),
    path('profile/', UserProfileView.as_view()),
]