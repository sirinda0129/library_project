import os
from django.shortcuts import get_object_or_404
# from rest_framework import status
from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from dotenv import load_dotenv
from posts.models import Group, Post # User

from .serializers import GroupSerializer, PostSerializer
from .telegram import send_telegram
# from .permissions import IsAuthorOrReadOnly

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")

class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(approved=True)
    serializer_class = PostSerializer
    def perform_create(self, serializer):
        serializer.save()
        send_telegram(CHAT_ID)

@api_view(["GET"])
def get_group(request, slug):
    if request.method == "GET":
        group = get_object_or_404(Group, slug=slug)
        posts = Post.objects.filter(group=group, approved=True)
        serializer = GroupSerializer(posts, many=True)
        return Response(serializer.data)
