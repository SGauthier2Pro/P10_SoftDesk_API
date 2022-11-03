"""
Contributor viewset class

    @get_queryset : returning contributors list by its project_ID
    @perform_create : create a contributor object for its project_id
                        POST method
    @update : update the contributor object by its ID PUT method
    @destroy : delete the contributor object by its ID DELETE method

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from projects.permissions import IsAuthenticated

from .multipleserializermixin import MultipleSerializerMixin

from projects.models.project import Project
from projects.models.contributor import Contributor

from projects.serializers.contributorserializer import ContributorSerializer


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Contributor.objects.filter(project_id=project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']

        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)

            if project.author_user_id == self.request.user:
                tmp_serializer = self.get_serializer(data=request.data)

                if User.objects.filter(
                        username=tmp_serializer.initial_data['user_id']
                ).exists():
                    user = User.objects.get(
                        username=tmp_serializer.initial_data['user_id'])
                    contributor = Contributor(
                        user_id=user,
                        project_id=project,
                        permission=tmp_serializer.initial_data['permission'],
                        role=tmp_serializer.initial_data['role']
                    )
                    contributor_data = self.serializer_class(
                        instance=contributor).data
                    serializer = self.get_serializer(data=contributor_data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED,
                                    headers=headers)
                else:
                    return Response({'username': "this user doesn't exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "You are not the project's "
                                            "author"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'project': "this project doesn't exists"},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']

        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)
            if project.author_user_id == self.request.user:
                if User.objects.filter(pk=self.kwargs['pk']).exists():
                    user = User.objects.get(pk=self.kwargs['pk'])
                    if Contributor.objects.filter(project_id=project_id,
                                                  user_id=user).exists():
                        Contributor.objects.filter(
                                project_id=project_id,
                                user_id=user
                            ).delete()
                        return Response(
                            {'message': 'The user has been delete from project'
                             },
                            status=status.HTTP_200_OK)
                    else:
                        return Response(
                            {'contributor': "this project/user relationship"
                                            " doesn't exists"},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'user': "this user_id doesn't exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "You are not the project's "
                                            "author"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'project': "this project_id doesn't exists"},
                            status=status.HTTP_400_BAD_REQUEST)
