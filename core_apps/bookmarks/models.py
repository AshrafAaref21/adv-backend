from django.db import models
from django.contrib.auth import get_user_model

from core_apps.articles.models import Article


User = get_user_model()


class Bookmark(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="bookmarks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("user", "article")
        ordering = ["-created_at"]
    

    def __str__(self) -> str:
        return f"{self.user.first_name.title()} bookmarked {self.article.title}"
    
