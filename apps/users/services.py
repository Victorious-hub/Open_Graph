from datetime import datetime, timezone
import uuid
from apps.users.models import PasswordReset, UserAccount
from django.contrib.auth.hashers import make_password

from core.exceptions import NotFoundError, PasswordNotMatchError, ResetLinkExpriredError


def user_create(*, email: str, password: str) -> UserAccount:
    """
    Create a new user account.
    Args:
        email (str): The email address of the user.
        password (str): The password for the user account.
    Returns:
        UserAccount: The newly created user account.
    """

    user = UserAccount.objects.create(email=email, password=make_password(password))
    user.save()
    return user


def user_password_change(
    *, user: UserAccount, old_password: str, new_password: str
) -> UserAccount:
    """
    Change the password for a user account.
    Args:
        user (UserAccount): The user account to change the password for.
        old_password (str): The current password of the user account.
        new_password (str): The new password to set for the user account.
    Returns:
        UserAccount: The updated user account with the new password.
    Raises:
        PasswordNotMatchError: If the old password does not match the current password of the user account.
    """

    if not user.check_password(old_password):
        raise PasswordNotMatchError

    user.set_password(new_password)
    user.save()
    return user


def user_password_reset(*, user_id: int, email: str) -> PasswordReset:
    """
    Resets the password for a user.
    Args:
        user_id (int): The ID of the user.
        email (str): The email address of the user.
    Returns:
        PasswordReset: The created PasswordReset object.
    Raises:
        NotFoundError: If no user account with the given email exists.
    """
    if not UserAccount.objects.filter(email=email).exists():
        raise NotFoundError

    token = uuid.uuid4()
    reset_link = f"0.0.0.0:8000/api/v1/users/password-reset-new/{token}"
    reset_url = PasswordReset.objects.create(
        token=token, user_id=user_id, reset_url=reset_link
    )
    reset_url.save()
    return reset_url


def user_password_set_new(
    *, user: UserAccount, token: str, password: str
) -> PasswordReset:
    """
    Set a new password for a user account.
    Args:
        user (UserAccount): The user account for which to set the new password.
        token (str): The token associated with the password reset request.
        password (str): The new password to set.
    Returns:
        PasswordReset: The password reset object associated with the token.
    Raises:
        ResetLinkExpiredError: If the password reset link has expired.
    """

    password_reset = PasswordReset.objects.get(token=token)
    if not password_reset.expriry_at > datetime.now(timezone.utc):
        raise ResetLinkExpriredError

    user.set_password(password)
    user.save()
    password_reset.delete()
    return user
