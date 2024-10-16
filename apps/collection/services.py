from apps.collection.models import Collection, LinkCollection
from apps.links.models import Link
from apps.users.models import UserAccount
from core.exceptions import NotFoundError
from core.utils import get_object


def collection_create(*, user: UserAccount, name: str, description: str) -> Collection:
    """
    Create a new collection.
    Args:
        user (UserAccount): The user account creating the collection.
        name (str): The name of the collection.
        description (str): The description of the collection.
    Returns:
        Collection: The newly created collection.
    """

    collection = Collection.objects.create(
        user=user, name=name, description=description
    )

    collection.save()
    return collection


def collection_update(
    *, user_id: int, collection_id: str, name: str, description: str
) -> Collection:
    """
    Update a collection with the given parameters.
    Args:
        user_id (int): The ID of the user who owns the collection.
        collection_id (str): The ID of the collection to be updated.
        name (str): The new name for the collection.
        description (str): The new description for the collection.
    Returns:
        Collection: The updated collection.
    Raises:
        NotFoundError: If the collection does not exist or if the user does not own the collection.
    """

    collection: Collection = get_object(Collection, id=collection_id)
    if collection is None or collection.user.id != user_id:
        raise NotFoundError

    collection_obj = Collection.objects.update(name=name, description=description)
    return collection_obj


def collection_delete(user_id: int, collection_id: int) -> None:
    """
    Delete a collection.
    Args:
        user_id (int): The ID of the user.
        collection_id (int): The ID of the collection.
    Raises:
        NotFoundError: If the collection does not exist or if the collection does not belong to the user.
    Returns:
        None
    """

    collection: Collection = get_object(Collection, id=collection_id)

    if collection is None or collection.user.id != user_id:
        raise NotFoundError
    collection.delete()


def link_collection_create(*, user_id: int, link_id: int, collection_id: int) -> None:
    """
    Add a link to a collection.
    Args:
        user_id (int): The ID of the user.
        link_id (int): The ID of the link to be added.
        collection_id (int): The ID of the collection to add the link to.
    Raises:
        NotFoundError: If the link or collection does not exist or if the user does not have access to them.
    Returns:
        None
    """

    link: Link = get_object(Link, id=link_id)
    collection: Collection = get_object(Collection, id=collection_id)

    if link is None or link.user.id != user_id:
        raise NotFoundError

    if collection is None or collection.user.id != user_id:
        raise NotFoundError

    link_collection = LinkCollection.objects.create(link=link, collection=collection)

    link_collection.save()
    return link_collection
