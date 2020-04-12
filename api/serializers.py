from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(many=True, read_only=True, slug_field="slug")
    class Meta:
        model = Post
        fields = ["id", "title", "description", "url", "group", "pub_date", "language"]
