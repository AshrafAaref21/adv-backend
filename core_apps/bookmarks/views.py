from uuid import UUID

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from django.db import IntegrityError

from .models import Bookmark
from .serializers import BookmarkSerializer
from core_apps.articles.models import Article


class BookmarkCreateView(CreateAPIView):
    """Bookmark create api view. | POST."""

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")

        if article_id:
            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError("Invalid article_id provided")

        else:
            raise ValidationError("article_id is required")

        try:
            serializer.save(user=self.request.user, article=article)

        except IntegrityError:
            raise ValidationError("You have already bookmarked this article.")


class BookmarkDestroyView(DestroyAPIView):
    """Delete Bookmarked article api view."""

    queryset = Bookmark.objects.all()
    lookup_field = "article_id"
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        article_id = self.kwargs.get("article_id")

        try:
            UUID(str(article_id), version=4)
        except ValueError:
            raise ValidationError("Invalid article_id provided")

        try:
            bookmark = Bookmark.objects.get(user=user, article__id=article_id)
            return bookmark

        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark not found or you don't own it.")

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.user != user:
            raise ValidationError("You cannot delete a bookmark that's not yours.")

        instance.delete()
