from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Group, Post, User

from .serializers import GroupSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.data["author"] == self.request.user:
            serializer.save()
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk):
        queryset = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(queryset, data=request.data, partial=True)
        if queryset.author == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
def get_group(request, slug):
    if request.method == "GET":
        group = get_object_or_404(Group, slug=slug)
        posts = Post.objects.filter(group=group)
        serializer = GroupSerializer(posts, many=True)
        return Response(serializer.data)
