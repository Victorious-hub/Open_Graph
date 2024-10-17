from apps.collection.models import Collection, LinkCollection
from apps.collection.selectors import (
    collection_get,
    collection_list,
    link_collection_list,
)
from apps.collection.services import (
    collection_create,
    collection_delete,
    collection_update,
    link_collection_create,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from core.utils import LimitOffsetPagination, get_paginated_response, inline_serializer


class CollectionCreateApi(views.APIView):
    """
    API endpoint for creating a collection. Requires authentication.
    Body Parameters:
        name (str): The name of the collection.
        description (str): The description of the collection.
    Returns:
        The HTTP response indicating the success of the collection creation.
    Methods:
        POST: Create a new collection.
    """

    permission_classes = [IsAuthenticated]

    class CollectionCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Collection
            exclude = ["user"]

    @extend_schema(
        request=CollectionCreateSerializer,
        responses={
            201: None,
            400: OpenApiResponse(description="Bad request. Invalid credentials"),
        },
        tags=["collections"],
        description="Create a new collection",
    )
    def post(self, request):
        serializer = self.CollectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection_create(user=request.user, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class CollectionGetApi(views.APIView):
    permission_classes = [IsAuthenticated]

    class CollectionGetSerializer(serializers.ModelSerializer):
        user = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
            }
        )

        class Meta:
            model = Collection
            fields = "__all__"

    @extend_schema(
        request=CollectionGetSerializer,
        responses={
            200: None,
            401: OpenApiResponse(description="User is not authenticated"),
            404: OpenApiResponse(description="Collection is not found"),
        },
        tags=["collections"],
        description="Retrieve a collection by ID",
    )
    def get(self, request, collection_id: int):
        data = self.CollectionGetSerializer(
            collection_get(user_id=request.user.pk, collection_id=collection_id)
        ).data
        return Response(data, status=status.HTTP_200_OK)


class CollectionListApi(views.APIView):
    """
    API endpoint for retrieving a list of collections. Requires authentication.
    Body Parameters:
        None
    Returns:
        The HTTP response containing the list of collections.
    Methods:
        GET: Retrieve a paginated list of collections.
    """

    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class CollectionListSerializer(serializers.ModelSerializer):
        user = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
            }
        )

        class Meta:
            model = Collection
            fields = "__all__"

    @extend_schema(
        request=CollectionListSerializer,
        responses={
            200: None,
            401: OpenApiResponse(description="User is not authenticated"),
        },
        tags=["collections"],
        description="Retrieve a paginated list of collections",
    )
    def get(self, request):
        data = self.CollectionListSerializer(
            collection_list(user_id=request.user.pk), many=True
        ).data
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.CollectionListSerializer,
            queryset=data,
            request=request,
            view=self,
        )


class CollectionDeleteApi(views.APIView):
    """
    API endpoint for deleting a collection. Requires authentication.
    Body Parameters:
        id (int): The ID of the collection to delete.
    Returns:
        The HTTP response indicating the success of the collection deletion.
    Methods:
        DELETE: Delete the specified collection.
    """

    permission_classes = [IsAuthenticated]

    class CollectionDeleteSerializer(serializers.Serializer):
        id = serializers.Serializer(required=True)

    @extend_schema(
        request=CollectionDeleteSerializer,
        responses={
            204: None,
            401: OpenApiResponse(description="User is not authenticated"),
            404: OpenApiResponse(description="Collection is not found"),
        },
        tags=["collections"],
        description="Delete a collection",
    )
    def delete(self, request, collection_id: int):
        collection_delete(user_id=request.user.id, collection_id=collection_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionUpdateApi(views.APIView):
    """
    API endpoint for updating a collection. Requires authentication.
    Body Parameters:
        name (str): The name of the collection.
        description (str): The description of the collection.
    Returns:
        The HTTP response indicating the success of the collection update.
    Methods:
        PUT: Update the specified collection.
    """

    permission_classes = [IsAuthenticated]

    class CollectionUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Collection
            exclude = ["user", "id", "created_at", "updated_at"]

    @extend_schema(
        request=CollectionUpdateSerializer,
        responses={
            200: None,
            401: OpenApiResponse(description="User is not authenticated"),
            404: OpenApiResponse(description="Collection is not found"),
        },
        tags=["collections"],
        description="Update a collection",
    )
    def put(self, request, collection_id: int):
        serializer = self.CollectionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection_update(
            user_id=request.user.id,
            collection_id=collection_id,
            **serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)


class LinkCollectionCreateApi(views.APIView):
    """
    API endpoint for creating a link collection.
    Body Parameters:
        link_id (int): The ID of the link.
        collection_id (int): The ID of the collection.
    Returns:
        The HTTP response indicating the success of the link collection creation.
    Methods:
        POST: Create a new link collection
    """

    permission_classes = [IsAuthenticated]

    class LinkCollectionCreateSerializer(serializers.Serializer):
        link_id = serializers.IntegerField()
        collection_id = serializers.IntegerField()

    @extend_schema(
        request=LinkCollectionCreateSerializer,
        responses={
            201: None,
            401: OpenApiResponse(description="User is not authenticated"),
            400: OpenApiResponse(description="Bad request. Invalid credentials"),
        },
        tags=["link_collections"],
        description="Create a new link collection",
    )
    def post(self, request):
        serializer = self.LinkCollectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link_collection_create(user_id=request.user.id, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class LinkCollectionListApi(views.APIView):
    """
    API endpoint for retrieving a list of link collections. Requires authentication.
    Body Parameters:
        None
    Returns:
        The HTTP response containing the list of link collections.
    Methods:
        GET: Retrieve a paginated list of link collections.
    """

    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class LinkCollectionListSerializer(serializers.ModelSerializer):
        collection = inline_serializer(
            fields={
                "name": serializers.CharField(),
                "description": serializers.CharField(),
            }
        )

        link = inline_serializer(
            fields={
                "link_url": serializers.URLField(),
                "title": serializers.CharField(),
                "description": serializers.CharField(),
                "image": serializers.URLField(),
                "link_type": serializers.CharField(),
            }
        )
        class Meta:
            model = LinkCollection
            fields = "__all__"

    @extend_schema(
        request=LinkCollectionListSerializer,
        responses={
            201: LinkCollectionListSerializer,
            401: OpenApiResponse(description="User is not authenticated"),
        },
        tags=["link_collections"],
        description="Retrieve a paginated list of link collections",
    )
    def get(self, request):
        data = self.LinkCollectionListSerializer(
            link_collection_list(user_id=request.user.id), many=True
        ).data
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.LinkCollectionListSerializer,
            queryset=data,
            request=request,
            view=self,
        )
