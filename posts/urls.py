from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<str:slug>", views.group_posts, name="group"),
    path("new/", views.new_post, name = "new_post"),
    path("api/", include("api.urls")),
    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:post_id>/edit/", views.post_edit, name="post_edit"),
]