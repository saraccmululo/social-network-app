
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("toggle_follow/<str:username>", views.toggle_follow, name="toggle_follow"),
    path("following_feed", views.following_feed, name="following_feed"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like")
]
