import os

from django.shortcuts import get_object_or_404
from dotenv import load_dotenv

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from posts.models import Group, Post

from .permissions import IsAdminOrReadOnly
from .serializers import PostSerializer, GroupSerializer
from .telegram import send_telegram


load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(approved=True)
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
        send_telegram(CHAT_ID)


class APIGroup(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        group = get_object_or_404(Group, slug=slug)
        posts = Post.objects.filter(group=group, approved=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    serializer_class = GroupSerializer