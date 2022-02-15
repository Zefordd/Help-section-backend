from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def instructions_schema():
    page_url = openapi.Parameter('page_url', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    return swagger_auto_schema(manual_parameters=[page_url])
