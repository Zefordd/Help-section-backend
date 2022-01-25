from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, max_mb: int):
        self.max_mb = max_mb

    def __call__(self, file):
        file_size_mb = file.size >> 20
        if file_size_mb > self.max_mb:
            msg = f'Maximum file size {self.max_mb} mb. Your file size: {file_size_mb} mb'
            raise ValidationError(msg)


@deconstructible
class NameFileValidator:
    def __init__(self, ban_list: set):
        self.ban_list = ban_list

    def __call__(self, file):
        file_name = file.name
        is_ban = any(symbol in file_name for symbol in self.ban_list)
        if is_ban:
            msg = f'The name of the uploaded file "{file_name}" contains the following characters: {self.ban_list}'
            raise ValidationError(msg)
