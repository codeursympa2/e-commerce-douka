from django.urls import path

from .views import *
urlpatterns = [
    path("logout", logout_view, name="logout"),
    path("", Login_view.as_view(), name="login"),
    path("register", Register_view.as_view(), name="register")
]
