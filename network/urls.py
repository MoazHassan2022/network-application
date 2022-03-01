
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPost", views.createPost, name="createPost"),
    path("Profile/<str:username>", views.Profile, name="Profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("Edit/<int:id>", views.Edit, name="Edit"),
    path("like/<int:id>", views.like, name="like"),
    path("unlike/<int:id>", views.unlike, name="unlike"),
    path("likeFollowing/<int:id>", views.likeFollowing, name="likeFollowing"),
    path("unlikeFollowing/<int:id>", views.unlikeFollowing, name="unlikeFollowing")
]
