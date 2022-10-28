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
        project = get_object_or_404(
            Project.objects.filter(id=project_id)
        )
        if project.author_user_id == self.request.user:
            tmp_serializer = self.get_serializer(data=request.data)
            user = get_object_or_404(
                User.objects.filter(
                    username=tmp_serializer.initial_data['user_id'])
            )
            contributor = Contributor(
                user_id=user,
                project_id=project,
                permission=tmp_serializer.initial_data['permission'],
                role=tmp_serializer.initial_data['role']
            )
            contributor_data = self.serializer_class(instance=contributor).data
            serializer = self.get_serializer(data=contributor_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response({'message': 'Forbidden action'},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(
            Project.objects.filter(id=project_id)
        )
        if project.author_user_id == self.request.user:
            tmp_serializer = self.get_serializer(data=request.data)
            user = get_object_or_404(
                User.objects.filter(
                    username=tmp_serializer.initial_data['user_id'])
            )
            Contributor.objects.filter(
                    project_id=project_id,
                    user_id=user
                ).delete()
            return Response(
                {'message': 'The user has been delete from project'},
                status=status.HTTP_200_OK
            )
        else:
            return Response({'message': 'Forbidden action'},
                            status=status.HTTP_403_FORBIDDEN)
