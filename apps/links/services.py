from apps.links.models import Link
from apps.users.models import UserAccount
from core.exceptions import LinkExistsError, NotFoundError
from core.utils import fetch_open_graph_data, get_object


def link_create(*, user: UserAccount, link: str) -> Link:
    """
    Create a new Link object with the provided user and link URL.
    Args:
        user (UserAccount): The user account associated with the link.
        link (str): The URL of the link.
    Returns:
        Link: The newly created Link object.
    Raises:
        None
    """
    if Link.objects.filter(link_url=link, user=user).exists():
        raise LinkExistsError

    og_data = fetch_open_graph_data(link)

    link_obj = Link.objects.create(
        user=user,
        link_url=link,
        title=og_data["title"],
        description=og_data["description"],
        image=og_data["image"],
        link_type=og_data["link_type"],
    )

    link_obj.save()
    return link


def link_delete(*, user_id: int, link_id: int) -> None:
    """
    Delete a link.
    Args:
        user_id (int): The ID of the user.
        link_id (int): The ID of the link to be deleted.
    Raises:
        NotFoundError: If the link does not exist or if the link does not belong to the specified user.
    Returns:
        None
    """

    link: Link = get_object(Link, id=link_id)

    if link is None or link.user.id != user_id:
        raise NotFoundError
    link.delete()


def link_update(
    *,
    user_id: int,
    link_id: str,
    link_url: str,
    title: str,
    description: str,
    link_type: str,
    image: str,
) -> Link:
    """
    Update a link with the specified details.
    Args:
        user_id (int): The ID of the user who owns the link.
        link_id (str): The ID of the link to be updated.
        link_url (str): The updated URL of the link.
        title (str): The updated title of the link.
        description (str): The updated description of the link.
        link_type (str): The updated type of the link.
        image (str): The updated image of the link.
    Returns:
        Link: The updated link object.
    Raises:
        NotFoundError: If the link does not exist or does not belong to the specified user.
    """

    link: Link = get_object(Link, id=link_id)

    if link is None or link.user.id != user_id:
        raise NotFoundError
    
    if link.link_url == link_url:
        raise LinkExistsError

    link_obj = Link.objects.update(
        link_url=link_url,
        title=title,
        description=description,
        image=image,
        link_type=link_type,
    )
    return link_obj
