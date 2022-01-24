from django.db import models


class FileAttachment(models.Model):
    name = models.CharField(max_length=510, default='', blank=True)
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.id}-{self.name})"
