import os

from dotenv import load_dotenv

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Group, Post

from api.permissions import IsAdminOrReadOnly
from api.serializers import PostSerializer, GroupSerializer
from api.telegram import send_telegram


load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(approved=True).order_by("-pub_date")
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group__slug',]

    def perform_create(self, serializer):
        serializer.save()
        send_telegram(CHAT_ID)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    serializer_class = GroupSerializer
