"""
serializer class for Contributor model

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.serializers import ModelSerializer

from projects.models.contributor import Contributor


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id',
                  'project_id',
                  'permission',
                  'role']
