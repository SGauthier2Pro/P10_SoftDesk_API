from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from projects.models.project import Project


class ProjectListSerializer(ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id',
                  'title',
                  'description',
                  'type',
                  'author_user_id']
        read_only_fields = ['id', 'author_user_id']

    def create(self, validated_data):
        project = Project.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author_user_id=self.context['request'].user
        )
        return project
