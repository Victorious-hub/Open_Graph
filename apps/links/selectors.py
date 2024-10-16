from apps.links.models import Link
from core.utils import get_object
from core.exceptions import NotFoundError


def link_get(*, user_id: int, link_id: int) -> Link:
    """
    Retrieve a link based on the provided user ID and link ID.
    Args:
        user_id (int): The ID of the user.
        link_id (int): The ID of the link.
    Returns:
        Link: The retrieved link.
    Raises:
        NotFoundError: If the link is not found or if the link does not belong to the specified user.
    """

    link = get_object(Link, id=link_id)

    if link is None or link.user.id != user_id:
        raise NotFoundError
    return link


def link_list(user_id: int) -> list[Link]:
    """
    Retrieve a list of links associated with a specific user.
    Args:
        user_id (int): The ID of the user.
    Returns:
        list[Link]: A list of Link objects filtered by the user ID.
    """

    link = Link.objects.filter(user__id=user_id)
    return link
