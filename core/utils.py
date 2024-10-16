from typing import Any, OrderedDict
from django.http import Http404
from django.shortcuts import get_object_or_404
import requests

from bs4 import BeautifulSoup

from apps.links.models import Link
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


def create_serializer_class(name: str, fields: dict) -> serializers.Serializer:
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields: dict, data: None = None, **kwargs) -> Any:
    """Function that outputs more complex data fields like foreign key relations etc."""

    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def get_object(model_or_queryset: Any, **kwargs) -> Any:
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


class LimitOffsetPagination(_LimitOffsetPagination):
    """
    Custom pagination class that extends `_LimitOffsetPagination`.
    Attributes:
        default_limit (int): The default number of items to be displayed per page.
        max_limit (int): The maximum number of items that can be displayed per page.
    Methods:
        get_paginated_data(data: dict) -> OrderedDict:
            Returns an ordered dictionary containing pagination information and the paginated data.
        get_paginated_response(data: dict) -> OrderedDict:
            Returns an ordered dictionary containing pagination information and the paginated response.
    """

    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data: dict) -> OrderedDict:
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data: dict) -> OrderedDict:
        return Response(
            OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


def get_paginated_response(
    *,
    pagination_class: Any,
    serializer_class: serializers.ModelSerializer,
    queryset: object,
    request: dict,
    view: str,
) -> Response:
    """
    Returns a paginated response for the given queryset.
    Args:
        pagination_class (Any): The pagination class to use.
        serializer_class (serializers.ModelSerializer): The serializer class to use.
        queryset (object): The queryset to paginate.
        request (dict): The request object.
        view (str): The view name.
    Returns:
        Response: The paginated response.
    """
    paginator = pagination_class()
    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(data=serializer.data)


def get_op_type(og_type: str) -> str:
    """
    Returns the operation type based on the given og_type.
    Parameters:
        og_type (str): The og_type to determine the operation type.
    Returns:
        str: The operation type.
    """

    for link_type in Link.LinkType:
        if link_type.value in og_type:
            return link_type.value
    return Link.LinkType.WEBSITE.value


def fetch_open_graph_data(url: str) -> dict:
    """
    Fetches Open Graph data from a given URL.
    Args:
        url (str): The URL to fetch Open Graph data from.
    Returns:
        dict: A dictionary containing the fetched Open Graph data. The dictionary has the following keys:
            - 'title': The title of the webpage.
            - 'description': The description of the webpage.
            - 'image': The URL of the image associated with the webpage.
            - 'link_type': The type of the webpage link.
    Raises:
        Exception: If there is an error fetching data from the URL.
    """
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching data from {url}: {e}")
    except requests.exceptions.Timeout:
        Exception("Request time out")
    else:
        og_data = {
            "title": None,
            "description": None,
            "image": None,
            "link_type": Link.LinkType.WEBSITE.value,
        }

        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")
        og_type = soup.find("meta", property="og:type")

        if og_title:
            og_data["title"] = og_title["content"]
        if og_description:
            og_data["description"] = og_description["content"]
        if og_image:
            og_data["image"] = og_image["content"]
        if og_type:
            og_data["link_type"] = get_op_type(og_type["content"])

        if not og_data["title"]:
            title_tag = soup.find("title")
            if title_tag:
                og_data["title"] = title_tag.text

        if not og_data["description"]:
            meta_description = soup.find("meta", attrs={"name": "description"})
            if meta_description:
                og_data["description"] = meta_description["content"]

        return og_data
