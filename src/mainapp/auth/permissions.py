from enum import Enum

from mainapp.auth import GroupName


class PermissionsEnum(str, Enum):
    TEST_1 = 'test'
    TEST_2 = 'test_2'

    @classmethod
    def all_values(cls) -> list[str]:
        return list(map(lambda p: p.value, cls))


P = PermissionsEnum
G = GroupName

PERMISSIONS_MAP = {
    G.admin: P.all_values(),
    G.moderator: [],
    G.client: [],
    G.manager: [],
}
