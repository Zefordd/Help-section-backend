from django.db.models import TextChoices


class ReferenceInfoStatus(TextChoices):
    published = 'published', 'Published'
    unpublished = 'unpublished', 'Unpublished'


class ArticleContentType(TextChoices):
    subtitle = 'subtitle', 'Subtitle'
    text = 'text', 'Text'
    video_url = 'video_url', 'Video url'
    image = 'image', 'Image'
