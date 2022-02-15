from attachment.models import FileAttachment
from attachment.serializers import FileAttachmentSerializer, FileSerializer, get_default_file_validators
from django.contrib.auth.models import Group
from help import models as help_models
from help.services.help_information_crud import update_section, update_subsection
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


class ArticleContentSerializer(serializers.ModelSerializer):
    subsection_id = serializers.PrimaryKeyRelatedField(
        queryset=help_models.Subsection.objects.all(), many=False, required=True, source='subsection'
    )
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=FileAttachment.objects.all(), source='image', write_only=True, required=False,
    )
    image = FileAttachmentSerializer(read_only=True, required=False)

    class Meta:
        model = help_models.ArticleContent
        fields = ('id', 'subsection_id', 'subtitle', 'text', 'video_url', 'order', 'content_type', 'image_id', 'image')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'name_ru')


class SubsectionSerializer(serializers.ModelSerializer):
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=help_models.Section.objects.all(), many=False, required=True, source='section'
    )
    article_content = ArticleContentSerializer(many=True, read_only=True)
    document_ids = serializers.PrimaryKeyRelatedField(
        queryset=FileAttachment.objects.all(), source='documents', write_only=True, required=False, many=True,
    )
    documents = FileAttachmentSerializer(read_only=True, required=False, many=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source='roles', write_only=True, required=False, many=True,
    )
    roles = RoleSerializer(read_only=True, required=False, many=True)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user
        update_subsection(instance, user, validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = help_models.Subsection
        fields = (
            'id',
            'section_id',
            'name',
            'status',
            'roles',
            'role_ids',
            'order',
            'document_ids',
            'documents',
            'article_content',
        )


class InstructionsSectionSerializer(serializers.ModelSerializer):
    subsections = serializers.SerializerMethodField()
    page_url = serializers.CharField(read_only=True)

    def get_subsections(self, obj):
        subsections = obj.subsections_with_roles
        serializer = _SectionSubsectionsSerializer(subsections, many=True)
        return serializer.data

    class Meta:
        model = help_models.Section
        fields = ('id', 'name', 'status', 'page_url', 'order', 'subsections')
