from enum import Enum

from mainapp.auth import GroupName


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
    G.client: [],
    G.manager: [],
}
