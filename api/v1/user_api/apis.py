from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.users.models import UserAccount
from apps.users.services import (
    user_create,
    user_password_change,
    user_password_reset,
    user_password_set_new,
)

from rest_framework import views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated



class TokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class ObtainTokenAPIView(views.APIView):
    """
    API view for obtaining a token.
    Body Parameters:
        email (str): The email of the user.
        password (str): The password of the user.
    Returns:
        The HTTP response containing tokens (access and refresh).
    Methods:
        POST: Login user and get tokens.
    """

    @extend_schema(
        request=TokenObtainPairSerializer,
        responses={
            201: TokenObtainPairSerializer,
            400: OpenApiResponse(description="Bad request. Invalid credentials"),
        },
        tags=["users"],
        description="Login user and get tokens",
    )
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data
        return Response(token_data, status=status.HTTP_201_CREATED)


class UserCreateApi(APIView):
    """
    API endpoint for creating a new user.
    Body Parameters:
        email (str): The email of the user.
        password (str): The password of the user.
    Returns:
        The HTTP response indicating the success of the user creation.
    Methods:
        POST: Create a new user.
    """

    class UserCreateSerializer(serializers.ModelSerializer):
        email = serializers.EmailField()
        password = serializers.CharField()

        class Meta:
            model = UserAccount
            fields = ["email", "password"]

    @extend_schema(
        request=UserCreateSerializer,
        responses={
            201: None,
            400: OpenApiResponse(description="Bad request. Invalid credentials"),
        },
        tags=["users"],
        description="Create a new user",
    )
    def post(self, request):
        serializer = self.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class ChangePasswordApi(views.APIView):
    """
    API endpoint for changing user password. Requires authentication.
    Body Parameters:
        old_password (str): The old password of the user.
        new_password (str): The new password of the user.
    Returns:
        The HTTP response indicating the success of the password change.
    Methods:
        PUT: Change user password.
    """

    permission_classes = [IsAuthenticated]

    class ChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: None,
            401: OpenApiResponse(description="User is not authenticated"),
            400: OpenApiResponse(description="Bad request. Invalid credentials"),
        },
        tags=["users"],
        description="Change user password",
    )
    def put(self, request):
        serializer = self.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_password_change(user=request.user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class PasswordResetApi(views.APIView):
    """
    API endpoint for resetting user password. Requires authentication.
    Body Parameters:
        email (str): The email of the user.
    Returns:
        The HTTP response indicating the success of the password reset request.
    Methods:
        POST: Reset user password.
    """

    permission_classes = [IsAuthenticated]

    class EmailSerializer(serializers.Serializer):
        email = serializers.EmailField()

    @extend_schema(
        request=EmailSerializer,
        responses={
            200: None,
            404: OpenApiResponse(description="User is not found"),
        },
        tags=["users"],
        description="Reset user password",
    )
    def post(self, request):
        serializer = self.EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_password_reset(user_id=request.user.pk, **serializer.validated_data)
        return Response(
            "Password reset link has been sent to your email", status=status.HTTP_200_OK
        )


class PasswordNewApi(views.APIView):
    """
    API endpoint for setting a new password. Requires authentication.
    Body Parameters:
        password (str): The new password of the user.
    Returns:
        The HTTP response indicating the success of the password change.
    Methods:
        POST: Set new password.
    """

    permission_classes = [IsAuthenticated]

    class NewPasswordSerializer(serializers.Serializer):
        password = serializers.CharField(required=True)

    @extend_schema(
        request=NewPasswordSerializer,
        responses={
            201: None,
            401: OpenApiResponse(description="User is not authenticated"),
            400: OpenApiResponse(description="Reset link expired"),
        },
        tags=["users"],
        description="Set new password for user",
    )
    def post(self, request, token: str):
        serializer = self.NewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_password_set_new(
            user=request.user, token=token, **serializer.validated_data
        )
        return Response(status=status.HTTP_201_CREATED)
