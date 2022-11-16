"""
serializer class for issue model
@create : function for adding author id at creation

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.serializers import ModelSerializer

from projects.models.issue import Issue


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id',
                  'title',
                  'desc',
                  'tag',
                  'priority',
                  'project_id',
                  'status',
                  'author_user_id',
                  'assignee_user_id',
                  'created_time']
        read_only_fields = ['id', 'author_user_id']

    def create(self, validated_data):
        issue = Issue.objects.create(
            title=validated_data['title'],
            desc=validated_data['desc'],
            tag=validated_data['tag'],
            priority=validated_data['priority'],
            project_id=validated_data['project_id'],
            status=validated_data['status'],
            author_user_id=self.context['request'].user,
            assignee_user_id=validated_data['assignee_user_id']
        )

        return issue
