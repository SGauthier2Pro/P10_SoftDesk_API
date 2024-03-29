"""
serializer class for Contributor model

@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from projects.models.contributor import Contributor


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id',
                  'project_id',
                  'permission',
                  'role']

    def validate(self, attributes):
        if Contributor.objects.filter(user_id=attributes['user_id'],
                                      project_id=attributes['project_id']
                                      ).exists():
            raise serializers.ValidationError(
                {"user": "User contribution relationship "
                         "with this project already exists."}
            )
        return attributes
