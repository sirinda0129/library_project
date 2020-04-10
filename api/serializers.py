from rest_framework import serializers

from posts.models import Group, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username")

    class Meta:
        model = Post
        fields = ["id", "title", "author", "description", "url", "group", "pub_date", "language"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "title", "slug", "description"]
