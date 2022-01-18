from django.db.models import Choices


class GroupName(Choices):
    admin = 'admin'
    moderator = 'moderator'
    client = 'client'
    manager = 'manager'
