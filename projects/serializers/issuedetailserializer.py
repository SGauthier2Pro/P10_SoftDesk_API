"""
serializer class for issue model
return the entire details of an issue
    @get_comments : included comment details

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.serializers import ModelSerializer, SerializerMethodField

from projects.serializers.commentserializer import CommentSerializer

from projects.models.issue import Issue


class IssueDetailSerializer(ModelSerializer):

    comments = SerializerMethodField()

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
                  'created_time',
                  'comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data
