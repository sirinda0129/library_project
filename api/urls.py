from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, get_group


router = DefaultRouter()
router.register(r"v1/posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("v1/group/<str:slug>/", get_group, name="group"),
    path("v1/api-token-auth", obtain_auth_token),
]
