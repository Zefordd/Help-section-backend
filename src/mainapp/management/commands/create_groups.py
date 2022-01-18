from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from mainapp.auth import PERMISSIONS_MAP, GroupName, PermissionsEnum
from mainapp.utils import get_title_cased_str


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Create or update roles and permissions
        """
        self.create_groups()

    def create_groups(self):
        self._create_groups()
        self._create_permissions()
        self._set_permissions_to_groups()

    def _create_groups(self):
        existing_groups = set(Group.objects.values_list('name', flat=True))
        groups_to_create = []
        for group_name in GroupName.all_values():
            if group_name not in existing_groups:
                groups_to_create.append(Group(name=group_name))
        if groups_to_create:
            print(f'The following Groups will be created: {", ".join([group.name for group in groups_to_create])}')
            Group.objects.bulk_create(groups_to_create)

    def _create_permissions(self):
        content_type = ContentType.objects.get(model='user')
        perms_by_codename = {perm.codename: perm for perm in Permission.objects.all()}
        perms_to_update = list()
        perms_to_create = list()
        for perm in PermissionsEnum.all_values():
            perm_data = {'codename': perm, 'content_type': content_type, 'name': get_title_cased_str(perm)}
            perm_instance = perms_by_codename.get(perm)
            if perm_instance is not None:
                perm_data.pop('codename')
                for attr_name, attr_value in perm_data.items():
                    setattr(perm_instance, attr_name, attr_value)
                perms_to_update.append(perm_instance)
            else:
                perms_to_create.append(Permission(**perm_data))

        if perms_to_update:
            Permission.objects.bulk_update(perms_to_update, fields=('content_type', 'name',))
        if perms_to_create:
            print(
                f'The following Permissions will be created: {", ".join([perm.codename for perm in perms_to_create])}'
            )
            Permission.objects.bulk_create(perms_to_create)

    def _set_permissions_to_groups(self):
        groups_by_name = {group.name: group for group in Group.objects.all()}
        perms_by_codenames = {perm.codename: perm for perm in Permission.objects.all()}
        for group_name, permissions_names in PERMISSIONS_MAP.items():
            group = groups_by_name[group_name]
            perm_instances = list()
            for perm_name in permissions_names:
                perm_instances.append(perms_by_codenames[perm_name])
            group.permissions.set(perm_instances)
