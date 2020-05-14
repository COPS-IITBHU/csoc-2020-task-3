from django.urls import path
from .views import LoginView, RegisterView, UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(),name="login-view"),
    path('register/', RegisterView.as_view(),name="register"),
    path('profile/', UserProfileView.as_view(),name="profile"),
]