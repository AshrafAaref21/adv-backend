from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView

from .views import CustomUserDetailsView

# app_name = 'users'


urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path("auth/user/", CustomUserDetailsView.as_view(), name="user-details"),
]
