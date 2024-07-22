from rest_framework import serializers

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark Base Serializer class."""

    article_title = serializers.CharField(source="article.title", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Bookmark
        fields = [
            "id",
            "user_first_name",
            "user_last_name",
            "article_title",
            "created_at",
        ]
        read_only_fields = ["user"]
