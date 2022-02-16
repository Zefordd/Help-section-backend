from drf_yasg import openapi
from drf_yasg.openapi import TYPE_OBJECT, Schema
from drf_yasg.utils import swagger_auto_schema


def instructions_schema():
    page_url = openapi.Parameter('page_url', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    return swagger_auto_schema(manual_parameters=[page_url])


def drag_and_drop_schema():
    return swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            description="An object where the key is the object's id and the value is the object's new order",
        )
    )
