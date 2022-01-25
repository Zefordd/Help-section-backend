from enum import Enum

from mainapp.auth import GroupName
from rest_framework import permissions

MAIN_APP_PREFIX = 'mainapp.'


def get_permission_for_check(permission, app_prefix=MAIN_APP_PREFIX):
    return f'{app_prefix}{permission}'


class Permissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': [],
        'PATCH': [],
        'DELETE': [],
    }

    def get_required_permissions(self, method, model_cls):
        return [get_permission_for_check(perm) for perm in super().get_required_permissions(method, model_cls)]


class PermissionsEnum(str, Enum):
    HELP_FULL_PERMISSIONS = 'help_full_permissions'

    @classmethod
    def all_values(cls) -> list[str]:
        return list(map(lambda p: p.value, cls))


P = PermissionsEnum
G = GroupName

PERMISSIONS_MAP = {
    G.admin: P.all_values(),
    G.content_manager: [P.HELP_FULL_PERMISSIONS],
    G.customer: [],
    G.manager: [],
}
