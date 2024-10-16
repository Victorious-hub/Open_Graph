from apps.collection.models import Collection, LinkCollection
from core.exceptions import NotFoundError
from core.utils import get_object


def collection_get(*, user_id: int, collection_id: int) -> Collection:
    """
    Retrieve a collection based on the provided user ID and collection ID.
    Args:
        user_id (int): The ID of the user.
        collection_id (int): The ID of the collection.
    Returns:
        Collection: The retrieved collection.
    Raises:
        NotFoundError: If the collection does not exist or if the user does not have access to it.
    """
    collection = get_object(Collection, id=collection_id)

    if collection is None or collection.user.id != user_id:
        raise NotFoundError
    return collection


def collection_list(user_id: int) -> list[Collection] | list:
    """
    Retrieve a list of collections for a given user ID.
    Parameters:
        user_id (int): The ID of the user.
    Returns:
        list[Collection]: A list of Collection objects filtered by the user ID.
    """
    collection = Collection.objects.filter(user__id=user_id)
    return collection


def link_collection_list(user_id: int) -> list[LinkCollection] | list:
    """
    Retrieve a list of collections for a given user ID.
    Parameters:
        user_id (int): The ID of the user.
    Returns:
        list[Collection]: A list of Collection objects filtered by the user ID.
    """
    link_collections = LinkCollection.objects.filter(collection__user__id=user_id)
    return link_collections
