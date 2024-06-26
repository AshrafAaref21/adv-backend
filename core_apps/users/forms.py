"""Forms module for custom user app."""

from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserChangeFrom(admin_forms.UserChangeForm):
    """Change form for users model."""
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationFrom(admin_forms.UserCreationForm):
    """Creation form for users model."""
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email")
    
    error_messages = {
        "duplicate_email" : "A user with this email already exists.",
    }

    def clean_email(self):
        """Check if the email is already exists."""
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
