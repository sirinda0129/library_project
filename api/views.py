from django.shortcuts import get_object_or_404
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Group, Post # User

from .serializers import GroupSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(["GET"])
def get_group(request, slug):
    if request.method == "GET":
        group = get_object_or_404(Group, slug=slug)
        posts = Post.objects.filter(group=group)
        serializer = GroupSerializer(posts, many=True)
        return Response(serializer.data)
