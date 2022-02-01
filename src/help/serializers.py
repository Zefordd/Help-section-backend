from attachment.serializers import FileSerializer, get_default_file_validators
from help import models as help_models
from help.services.help_information_crud import update_section
from rest_framework import serializers


class HelpDocumentSerializer(FileSerializer):
    file = serializers.FileField(validators=get_default_file_validators(['pdf', 'doc', 'docx', 'doc', 'xlsx', 'xls']))


class _SectionSubsectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = help_models.Subsection
        fields = ('id', 'name', 'order', 'status')


class SectionSerializer(serializers.ModelSerializer):
    subsections = serializers.SerializerMethodField()
    page_url = serializers.CharField(read_only=True)

    def get_subsections(self, obj):
        subsections = obj.subsections.filter(deleted_at__isnull=True).all()
        serializer = _SectionSubsectionsSerializer(subsections, many=True)
        return serializer.data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        instance = super().create(validated_data)
        help_models.Subsection.objects.create(
            section=instance, name='New section', order=1, created_by=instance.created_by
        )
        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user
        update_section(instance, user, validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = help_models.Section
        fields = ('id', 'name', 'status', 'page_url', 'order', 'subsections')
