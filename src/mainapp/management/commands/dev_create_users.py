from functools import cached_property

from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from mainapp.management.data.users import get_dev_user_list
from mainapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_users()

    def create_users(self):
        existing_users = set(User.objects.values_list('username', flat=True))
        for user_data in get_dev_user_list():
            password = user_data.pop('password')
            group_names = user_data.pop('groups')
            if user_data['username'] not in existing_users:
                user = User(**user_data)
                user.set_password(password)
                user.save()
                groups = self.get_group_instances(group_names)
                user.groups.set(groups)

    @cached_property
    def groups_map(self) -> dict[str, Group]:
        return {group.name: group for group in Group.objects.all()}

    def get_group_instances(self, group_names: list[str]) -> list[Group]:
        return [self.groups_map[group_name] for group_name in group_names]
