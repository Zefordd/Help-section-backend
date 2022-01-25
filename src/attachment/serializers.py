from typing import Optional, Sequence

from attachment.constance import FILE_NAME_BAN_LIST
from attachment.custom_validators import MaxFileSizeValidator, NameFileValidator
from attachment.models import FileAttachment
from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = '__all__'
        extra_kwargs = {'name': {'read_only': True}}
        ref_name = None


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = ('file',)
        extra_kwargs = {'file': {'required': True}}


def get_default_file_validators(
    allowed_extensions: Sequence[str], max_mb: Optional[int] = 50, ban_list: Optional[set[str]] = FILE_NAME_BAN_LIST
) -> list:
    if not allowed_extensions:
        raise ValueError('allowed_extensions cannot be empty')
    validators = [FileExtensionValidator(allowed_extensions=allowed_extensions)]
    if max_mb:
        validators.append(MaxFileSizeValidator(max_mb=max_mb))
    if ban_list:
        validators.append(NameFileValidator(ban_list=ban_list))
    return validators


class DocumentsSerializer(FileSerializer):
    file = serializers.FileField(validators=get_default_file_validators(['pdf', 'doc', 'docx']))


class ImagesSerializer(FileSerializer):
    file = serializers.FileField(validators=get_default_file_validators(['jpg', 'jpeg', 'jpe', 'png', 'bmp']))
