from django.db.models.query import FlatValuesListIterable


def get_title_cased_str(string: str) -> str:
    """
    Convert snakecased string to a titlecased string
    """
    return string.replace('_', ' ').title()


def get_user_roles(user) -> FlatValuesListIterable:
    return user.groups.values_list('name', flat=True)
