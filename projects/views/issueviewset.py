from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .multipleserializermixin import MultipleSerializerMixin

from projects.permissions import IsAuthenticated

from projects.models.project import Project
from projects.models.issue import Issue
from projects.models.contributor import Contributor

from projects.serializers.issuelistserializer import IssueListSerializer
from projects.serializers.issuedetailserializer import IssueDetailSerializer


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Issue.objects.filter(project_id=project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']

        project = get_object_or_404(
            Project.objects.filter(id=project_id)
        )

        contributors = Contributor.objects.filter(project_id=project.id)
        for contributor in contributors:
            if contributor.user_id == self.request.user:

                serializer = self.get_serializer(
                    data={'project_id': project.id,
                          'author_user_id': self.request.user.id,
                          'title': request.data['title'],
                          'desc': request.data['desc'],
                          'tag': request.data['tag'],
                          'priority': request.data['priority'],
                          'status': request.data['status'],
                          'assignee_user_id': request.data['assignee_user_id']
                          }
                )
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        return Response({'message': "Vous n'êtes pas contributeur "
                                    "de ce projet"},
                        status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if instance.project_id.id == int(project_id):
            if instance.author_user_id.id == self.request.user.id:

                instance = serializer.save()
                self.perform_update(instance)
                headers = self.get_success_headers(serializer.validated_data)
                return Response(serializer.data,
                                status=status.HTTP_206_PARTIAL_CONTENT,
                                headers=headers)
            else:
                return Response(
                    {'message': "Vous n'êtes pas authorisé à"
                                " modifier ce probleme"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {
                    'message': "ce problème n'existe pas pour ce projet"},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        instance = self.get_object()
        user = request.user
        if instance.project_id.id == int(project_id):
            if instance.author_user_id == user:
                self.perform_destroy(instance)
                return Response(
                    {'message': 'Le problème a bien été supprimer'},
                    status=status.HTTP_200_OK)
            else:
                return Response({'message': "Vous n'êtes pas autorisé à "
                                            "supprimer ce problème"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(
                {
                    'message': "ce problème n'existe pas pour ce projet"},
                status=status.HTTP_404_NOT_FOUND
            )
