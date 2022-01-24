from django.db.models import TextChoices


class ReferenceInfoStatus(TextChoices):
    published = 'published', 'Published'
    unpublished = 'unpublished', 'Unpublished'
