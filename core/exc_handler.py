from typing import Any
from core.exceptions import UnauthorizedError
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc: Any, context: Any) -> Response | None:
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

        # Add raise if user is Unauthorized
        if response.status_code == 401:
            return Response({"detail": UnauthorizedError().default_detail}, status=401)

    return response
