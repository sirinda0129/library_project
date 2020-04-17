from rest_framework import serializers

from posts.models import Group, Post


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug")

    class Meta:
        model = Post
        fields = ["id", "title", "description",
                  "url", "group", "pub_date", "language"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "title", "description", "slug"]
