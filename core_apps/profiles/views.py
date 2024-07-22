# TODO: change this in production
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authers_api.settings.local import DEFAULT_FROM_EMAIL

from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    """List view for Profile model."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = [ProfilesJSONRenderer]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """single profile view."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        return Profile.objects.select_related("user")

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.RetrieveAPIView):
    """Update user profile view."""

    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    """List of followers view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Get Method."""
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data,
            }

            return Response(formatted_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)


class FollowingListView(APIView):
    """List of followings view."""

    def get(self, request, user_id, format=None):
        """Get Method."""
        try:
            profile = Profile.objects.get(user__id=user_id)
            following_profiles = profile.following.all()
            users = [p.user for p in following_profiles]

            serializer = FollowingSerializer(users, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profiles.count(),
                "users_i_follow": serializer.data,
            }

            return Response(formatted_response, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)


class FollowAPIView(APIView):
    """Follow view."""

    def post(self, request, user_id, format=None):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if profile == follower:
                raise CantFollowYourself()

            if user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"""You're already following {profile.user.first_name.title()} {profile.user.last_name.title()}""",
                }

                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)

            subject = "A new User follows you"
            message = f"Hi {request.user.first_name}, the user {user_profile.user.get_full_name}  now follows you"
            from_email = DEFAULT_FROM_EMAIL
            recipients_list = [profile.user.email]

            send_mail(subject, message, from_email, recipients_list, fail_silently=True)

            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": f"You are following {profile.user.first_name} {profile.user.last_name}",
                },
                status=status.HTTP_200_OK,
            )

        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile doesn't exists.")


class UnfollowAPIVIEW(APIView):
    """Unfollow view."""

    def post(self, request, user_id, *args, **kargs):
        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if not user_profile.check_following(profile):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"You can't unfollow {profile.user.get_full_name}, since you were not following him in te first place.",
            }

            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        user_profile.unfollow(profile)
        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}",
            },
            status=status.HTTP_200_OK,
        )
