from django.urls import path

from .apis import LinkCreateApi, LinkDeleteApi, LinkGetApi, LinkListApi, LinkUpdateApi

urlpatterns = [
    path("", LinkCreateApi.as_view(), name="create-link"),
    path("list", LinkListApi.as_view(), name="list-link"),
    path("<int:link_id>", LinkGetApi.as_view(), name="get-link"),
    path("delete/<int:link_id>", LinkDeleteApi.as_view(), name="delete-link"),
    path("update/<int:link_id>", LinkUpdateApi.as_view(), name="update-link"),
]
