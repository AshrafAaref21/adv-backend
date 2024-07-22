from django.urls import path

from .views import ResponseListCreateView, ResposeUpdateDeleteView


urlpatterns = [
    path(
        "article/<uuid:article_id>/",
        ResponseListCreateView.as_view(),
        name="article-responses",
    ),
    path("<uuid:id>/", ResposeUpdateDeleteView.as_view(), name="detail-response"),
]
