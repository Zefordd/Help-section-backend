from attachment.serializers import FileSerializer, get_default_file_validators
from rest_framework import serializers


class HelpDocumentSerializer(FileSerializer):
    file = serializers.FileField(validators=get_default_file_validators(['pdf', 'doc', 'docx', 'doc', 'xlsx', 'xls']))
