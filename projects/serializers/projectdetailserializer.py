"""
serializer class for project model
return the entire details of a project
    @get_issues : included issues details
    @get_contributors : included contributors list

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.serializers import ModelSerializer, SerializerMethodField

from projects.serializers.issuedetailserializer import IssueDetailSerializer
from projects.serializers.contributorserializer import ContributorSerializer

from projects.models.project import Project


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
