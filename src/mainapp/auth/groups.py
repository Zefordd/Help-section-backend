from django.db.models import TextChoices


class GroupName(TextChoices):
    admin = 'admin'
    content_manager = 'content_manager'
    client = 'client'
    manager = 'manager'

    @classmethod
    def all_values(cls) -> list[str]:
        return list(map(lambda p: p.value, cls))
