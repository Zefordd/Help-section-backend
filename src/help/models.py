from attachment.models import FileAttachment
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from help.constants import ArticleContentType, ReferenceInfoStatus
from help.managers import SectionManager, SubsectionManager


class LastActionModel(models.Model):
    created_by = models.ForeignKey(
        'mainapp.User', on_delete=models.SET_NULL, related_name='created_%(class)ss', null=True, blank=True
    )
    updated_by = models.ForeignKey(
        'mainapp.User', on_delete=models.SET_NULL, related_name='updated_%(class)ss', null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Section(LastActionModel):
    name = models.CharField(max_length=250)
    status = models.CharField(
        choices=ReferenceInfoStatus.choices, max_length=120, default=ReferenceInfoStatus.unpublished
    )
    page_url = models.CharField(max_length=250, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SectionManager()

    def get_max_order(self):
        return self._meta.model.objects.aggregate(max_num=models.Max('order'))['max_num']

    def is_released(self):
        return self.status == ReferenceInfoStatus.published

    class Meta:
        ordering = ('order', 'id')


class Subsection(LastActionModel):
    section = models.ForeignKey(Section, related_name='subsections', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    status = models.CharField(
        choices=ReferenceInfoStatus.choices, max_length=120, default=ReferenceInfoStatus.unpublished
    )
    roles = models.ManyToManyField(to=Group, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)
    documents = models.ManyToManyField(to=FileAttachment, blank=True, related_name='subsection_documents')

    objects = SubsectionManager()

    def get_max_order(self):
        return self._meta.model.objects.filter(section=self.section).aggregate(max_num=models.Max('order'))['max_num']

    def is_released(self):
        return self.status == ReferenceInfoStatus.published

    class Meta:
        ordering = ('order', 'id')


class ArticleContent(LastActionModel):
    subsection = models.ForeignKey(Subsection, related_name='article_content', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    content_type = models.CharField(
        max_length=120, choices=ArticleContentType.choices, default=ArticleContentType.subtitle
    )
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        FileAttachment, on_delete=models.SET_NULL, blank=True, null=True, related_name='article_image'
    )

    def has_content(self):
        if self.content_type == ArticleContentType.image:
            return self.image_id is not None
        field_content = getattr(self, self.content_type)
        return field_content != '' and field_content is not None

    class Meta:
        ordering = ('order', 'id')
