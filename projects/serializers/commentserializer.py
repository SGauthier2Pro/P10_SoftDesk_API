"""
serializer class for comment model

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.serializers import ModelSerializer

from projects.models.comment import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id',
                  'description',
                  'author_user_id',
                  'issue_id',
                  'created_time']
        read_only_fields = ['id', 'author_user_id']