from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, get_group


router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("group/<str:slug>/", get_group, name="group"),
]
