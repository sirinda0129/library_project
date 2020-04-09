from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/add-group/", views.add_group, name="add_group"),
    path("group/<str:slug>/", views.group_posts, name="group"),
    path("profile/<username>/", views.profile, name="profile"),
    path("posts/<int:post_id>/", views.post_view, name="post"),
    path("posts/new/", views.new_post, name="new_post"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
]
