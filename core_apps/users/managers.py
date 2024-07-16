"""Definnig custom user manager."""

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUsermanager(BaseUserManager):
    """Custom user Manager."""

    def email_validator(self, email):
        """email validator function."""
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """Create user function."""
        if not first_name:
            raise ValueError(_("users must have a first name."))

        if not last_name:
            raise ValueError(_("users must have a last name."))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("users must have an email address."))

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """Create super admin user function."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("super user must have is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("super user must have is_superuser=True"))

        if not password:
            raise ValueError(_("superuser must have password"))

        if email:
            email = self.normalize_email(email)
        else:
            raise ValueError(_("super user must have an email address."))

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )

        user.save(using=self._db)
        return user
