from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from apps.links.services import link_create, link_delete, link_update
from apps.links.models import Link
from apps.links.selectors import link_get, link_list
from core.utils import LimitOffsetPagination, get_paginated_response, inline_serializer


class LinkCreateApi(views.APIView):
    """
    API endpoint for creating a link. Requires authentication.
    Body Parameters:
        link (str): The URL of the link to be created.
    Returns:
        The HTTP response indicating the success of the link creation.
    Methods:
        POST: Create a new link.
    """

    permission_classes = [IsAuthenticated]

    class LinkInputSerializer(serializers.Serializer):
        link = serializers.URLField()

    @extend_schema(
        request=LinkInputSerializer,
        responses={
            201: None,
            401: OpenApiResponse(description="User is not authenticated"),
        },
        tags=["links"],
        description="Create a new link",
    )
    def post(self, request):
        serializer = self.LinkInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link_create(user=request.user, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class LinkListApi(views.APIView):
    """
    API endpoint for retrieving a list of links. Requires authentication.
    Body Parameters:
        None
    Returns:
        The HTTP response containing the list of links.
    Methods:
        GET: Retrieve a paginated list of links.
    """

    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class LinkListOutputSerializer(serializers.ModelSerializer):
        user = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
            }
        )

        class Meta:
            model = Link
            fields = "__all__"

    @extend_schema(
        request=LinkListOutputSerializer,
        responses={
            200: LinkListOutputSerializer,
            401: OpenApiResponse(description="User is not authenticated"),
        },
        tags=["links"],
        description="Retrieve a paginated list of links",
    )
    def get(self, request):
        data = self.LinkListOutputSerializer(
            link_list(user_id=request.user.pk), many=True
        ).data
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.LinkListOutputSerializer,
            queryset=data,
            request=request,
            view=self,
        )


class LinkGetApi(views.APIView):
    """
    API endpoint for retrieving a specific link. Requires authentication.
    Body Parameters:
        link_id (int): The ID of the link to retrieve.
    Returns:
        Response object containing the link data.
    Methods:
        GET: Retrieve a specific link.
    """

    permission_classes = [IsAuthenticated]

    class LinkOutputSerializer(serializers.ModelSerializer):
        user = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
            }
        )

        class Meta:
            model = Link
            fields = "__all__"

    @extend_schema(
        request=LinkOutputSerializer,
        responses={
            200: LinkOutputSerializer,
            401: OpenApiResponse(description="User is not authenticated"),
            404: OpenApiResponse(description="User is not found"),
        },
        tags=["links"],
        description="Retrieve a specific link",
    )
    def get(self, request, link_id: int):
        data = self.LinkOutputSerializer(
            link_get(user_id=request.user.pk, link_id=link_id)
        ).data
        return Response(data, status=status.HTTP_200_OK)


class LinkDeleteApi(views.APIView):
    """
    API endpoint for deleting a link. Requires authentication.
    Body Parameters:
        link_id (int): The ID of the link to delete.
    Returns:
        The HTTP response indicating the success of the link deletion.
    Methods:
        DELETE: Deletes the specified link.
    """

    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={
            204: None,
            401: OpenApiResponse(description="User is not authenticated"),
            404: OpenApiResponse(description="User is not found"),
        },
        tags=["links"],
        description="Delete the specified link",
    )
    def delete(self, request, link_id: int):
        link_delete(user_id=request.user.id, link_id=link_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LinkUpdateApi(views.APIView):
    """
    API endpoint for updating a Link object. Requires authentication.
    Body Parameters:
        link_url (str): The URL of the link.
        title (str): The title of the link.
        description (str): The description of the link.
        image (str): The image URL of the link.
        link_type (str): The type of the link.
    Returns:
        The HTTP response indicating the success of the link update.
    Methods:
        PUT: Update the specified link
    """

    permission_classes = [IsAuthenticated]

    class LinkUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Link
            exclude = ["user", "id", "created_at", "updated_at"]

    @extend_schema(
        request=LinkUpdateSerializer,
        responses={
            200: None,
            401: OpenApiResponse(description="User is not authenticated"),
            404: OpenApiResponse(description="User is not found"),
        },
        tags=["links"],
        description="Update the specified link",
    )
    def put(self, request, link_id: int):
        serializer = self.LinkUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link_update(
            user_id=request.user.id, link_id=link_id, **serializer.validated_data
        )
        return Response(status=status.HTTP_200_OK)
