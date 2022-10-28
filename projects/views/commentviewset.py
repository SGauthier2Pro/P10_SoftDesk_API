from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from projects.permissions import IsAuthenticated

from .multipleserializermixin import MultipleSerializerMixin

from projects.models.project import Project
from projects.models.issue import Issue
from projects.models.comment import Comment
from projects.models.contributor import Contributor

from projects.serializers.commentserializer import CommentSerializer


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        issue_id = self.kwargs['issue_id']
        issue = get_object_or_404(Issue.objects.filter(id=issue_id))
        if issue.project_id.id == int(project_id):
            queryset = Comment.objects.filter(issue_id=issue_id)
            return queryset
        else:
            raise Http404("Ce problème n'existe pas pour ce projet")

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(
            Project.objects.filter(id=project_id)
        )
        issue_id = self.kwargs['issue_id']
        issue = get_object_or_404(
            Issue.objects.filter(id=int(issue_id))
        )
        contributors = Contributor.objects.filter(project_id=project.id)
        for contributor in contributors:
            if contributor.user_id == self.request.user:
                serializer = self.get_serializer(
                    data={'description': request.data['description'],
                          'author_user_id': self.request.user.id,
                          'issue_id': issue.id,
                          }
                )
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=headers)
        return Response({'message': "Vous n'êtes pas "
                                    "contributeur de ce projet"},
                        status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        issue_id = self.kwargs['issue_id']
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if instance.issue_id.id == int(issue_id):
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
                                " modifier ce commentaire"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {
                    'message': "ce commentaire n'existe pas pour ce problème"},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        issue_id = self.kwargs['issue_id']
        instance = self.get_object()
        user = request.user
        if instance.issue_id.id == int(issue_id):
            if instance.author_user_id == user:
                self.perform_destroy(instance)
                return Response(
                    {'message': 'Le commentaire a bien été supprimer'},
                    status=status.HTTP_200_OK)
            else:
                return Response({'message': "Vous n'êtes pas authorisé à"
                                " supprimer ce commentaire"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(
                {
                    'message': "ce commentaire n'existe pas pour ce problème"},
                status=status.HTTP_404_NOT_FOUND
            )
