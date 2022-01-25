from mainapp.auth import PermissionsEnum
from mainapp.auth.permissions import Permissions


class HelpPermission(Permissions):
    perms_map = {
        'GET': [PermissionsEnum.HELP_FULL_PERMISSIONS],
        'OPTIONS': [PermissionsEnum.HELP_FULL_PERMISSIONS],
        'HEAD': [PermissionsEnum.HELP_FULL_PERMISSIONS],
        'POST': [PermissionsEnum.HELP_FULL_PERMISSIONS],
        'PUT': [PermissionsEnum.HELP_FULL_PERMISSIONS],
        'PATCH': [PermissionsEnum.HELP_FULL_PERMISSIONS],
        'DELETE': [PermissionsEnum.HELP_FULL_PERMISSIONS],
    }
