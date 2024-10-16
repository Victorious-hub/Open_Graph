from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from .managers import UserAccountManager


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserAccountManager()

    def __str__(self):
        return f"User: {self.email}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class PasswordReset(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    reset_url = models.URLField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    expriry_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=1)
    )

    def __str__(self) -> str:
        return f"PasswordReset: {self.reset_url}"

    class Meta:
        verbose_name = "password reset"
        verbose_name_plural = "password resets"
