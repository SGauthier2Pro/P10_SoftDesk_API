from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from projects.models import Project, Issue, Comment, Contributor


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


class ProjectDetailSerializer(ModelSerializer):

    contributors = SerializerMethodField()
    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id',
                  'title',
                  'description',
                  'type',
                  'author_user_id',
                  'contributors',
                  'issues'
                  ]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueDetailSerializer(queryset, many=True)
        return serializer.data

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id',
                  'desc',
                  'tag',
                  'priority',
                  'project_id',
                  'status',
                  'author_user_id',
                  'assignee_user_id',
                  'created_time']


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id',
                  'desc',
                  'tag',
                  'priority',
                  'project_id',
                  'status',
                  'author_user_id',
                  'assignee_user_id',
                  'created_time',
                  'comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id',
                  'description',
                  'author_user_id',
                  'issue_id',
                  'created_time']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id',
                  'project_id',
                  'permission',
                  'role']

