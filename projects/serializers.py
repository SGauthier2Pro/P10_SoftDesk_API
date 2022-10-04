from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from projects.models import Project, Issue, Comment, Contributor


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id',
                  'title',
                  'description',
                  'type',
                  'author_user_id']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fiels = ['id',
                 'desc',
                 'tag',
                 'priority',
                 'project_id',
                 'status',
                 'author_user_id',
                 'assignee_user_id',
                 'created_time']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id',
                  'description',
                  'author_user_id',
                  'issue_id',
                  'created_time']
