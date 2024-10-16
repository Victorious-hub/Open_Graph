from django.urls import path

from .apis import (
    ChangePasswordApi,
    ObtainTokenAPIView,
    PasswordNewApi,
    PasswordResetApi,
    UserCreateApi,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", UserCreateApi.as_view(), name="create-user"),
    path("authenticate", ObtainTokenAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("password", ChangePasswordApi.as_view(), name="change-password"),
    path("password-reset", PasswordResetApi.as_view(), name="reset-password"),
    path(
        "password-reset-new/<str:token>",
        PasswordNewApi.as_view(),
        name="reset-password",
    ),
]
