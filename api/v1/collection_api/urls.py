from django.urls import path

from api.v1.collection_api.apis import (
    CollectionCreateApi,
    CollectionDeleteApi,
    CollectionGetApi,
    CollectionListApi,
    CollectionUpdateApi,
    LinkCollectionCreateApi,
    LinkCollectionListApi,
)

urlpatterns = [
    path("", CollectionCreateApi.as_view(), name="create-collection"),
    path("<int:collection_id>", CollectionGetApi.as_view(), name="get-collection"),
    path("list", CollectionListApi.as_view(), name="list-collection"),
    path(
        "update/<int:collection_id>",
        CollectionUpdateApi.as_view(),
        name="update-collection",
    ),
    path(
        "delete/<int:collection_id>",
        CollectionDeleteApi.as_view(),
        name="delete-collection",
    ),
    path("link", LinkCollectionCreateApi.as_view(), name="create-link-collection"),
    path("link/list", LinkCollectionListApi.as_view(), name="list-link-collections"),
]
