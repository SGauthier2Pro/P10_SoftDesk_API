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
        