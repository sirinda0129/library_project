from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import GroupViewSet, PostViewSet


router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register("group", GroupViewSet, basename="group")

urlpatterns = [
    path("", include(router.urls)),
]
