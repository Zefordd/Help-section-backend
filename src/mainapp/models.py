from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'))

    def __str__(self):
        return self.username
