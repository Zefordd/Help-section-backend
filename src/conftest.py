import pytest
from django.core.management import call_command
from mainapp.auth import GroupName
from mainapp.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def monkeypatch_session_fixture(request):
    from _pytest.monkeypatch import MonkeyPatch

    m_patch = MonkeyPatch()
    yield m_patch
    m_patch.undo()


@pytest.fixture(autouse=True)
def _automatic_django_db(db):
    """
    Mark all tests as tests that require database access
    """


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker, monkeypatch_session_fixture):
    with django_db_blocker.unblock():
        call_command('create_groups')
        call_command('dev_create_users')


def auth_client(client: APIClient, username: str):
    user = User.objects.get(username=username)
    client.force_authenticate(user)
    return client


def get_groups_statuses_map(
    custom_roles_statuses: dict[GroupName, int], default_status: int = status.HTTP_403_FORBIDDEN
) -> list[tuple[GroupName, int]]:
    mapping = []
    for group in GroupName:
        if group not in custom_roles_statuses:
            mapping.append((group, default_status))
    for role, status_code in custom_roles_statuses.items():
        mapping.append((role, status_code))
    return mapping
