from django.urls import path
from django.contrib.auth import views as auth_views

from .import views
from .views import LoginView, CustomLogoutView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
