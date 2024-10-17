from rest_framework.exceptions import APIException


class NotFoundError(APIException):
    status_code = 404
    default_detail = "Not Found"
    default_code = "not_found"


class PasswordNotMatchError(APIException):
    status_code = 400
    default_detail = "Passwords not match"
    default_code = "password_not_match"


class ResetLinkExpriredError(APIException):
    status_code = 400
    default_detail = "Reset link expired"
    default_code = "reset_link_expired"


class UnauthorizedError(APIException):
    status_code = 401
    default_detail = "Unauthorized"
    default_code = "unauthorized"


class LinkExistsError(APIException):
    status_code = 400
    default_detail = "Link already exists for the user"
    default_code = "bad_request"

class UserExistsError(APIException):
    status_code = 400
    default_detail = "User already exists"
    default_code = "bad_request"