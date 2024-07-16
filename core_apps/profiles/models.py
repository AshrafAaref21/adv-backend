"""Profile Model for User Profile app."""

from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampeModel


User = get_user_model()


class Profile(TimeStampeModel):
    """Profile Model."""

    class Gender(models.TextChoices):
        MALE = ("M", _("Male"))
        FEMALE = ("F", _("Female"))
        OTHER = ("O", _("Other"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+201281833318"
    )
    about_me = models.TextField(verbose_name=_("about me"), default="about you")
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=("country"), default="EG", null=False, blank=False
    )
    city = models.CharField(
        verbose_name=_("country"),
        default="Alexandria",
        blank=False,
        null=False,
        max_length=50,
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Image"), default="/profile_default.png"
    )
    twitter_handle = models.CharField(
        verbose_name=_("Twitter Handle"), max_length=20, blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile."

    def follow(self, profile):
        """Follow Method"""
        self.followers.add(profile)

    def unfollow(self, profile):
        """Unfollow Method"""
        self.followers.remove(profile)

    def check_following(self, profile):
        """check if the user follow another user."""
        return self.followers.filter(pkid=profile.pkid).exists()
