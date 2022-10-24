from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from rest_framework.decorators import permission_classes

from projects.permissions import IsAuthenticated, \
    IsAuthor, \
    IsProjectContributor
from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import ProjectListSerializer, \
    ProjectDetailSerializer, \
    IssueListSerializer, \
    IssueDetailSerializer, \
    CommentSerializer, \
    ContributorSerializer


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' \
                and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.filter(contributors__user_id=user.id)
        return queryset

    def perform_create(self, serializer):

        projet = serializer.save()

        contributor = Contributor.objects.create(
            user_id=self.request.user,
            project_id=projet,
            permission='author',
            role='author'
        )
        contributor.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance.author_user_id.id == self.request.user.id:

            instance = serializer.save()
            self.perform_update(instance)
            headers = self.get_success_headers(serializer.validated_data)
            return Response(serializer.data,
                            status=status.HTTP_206_PARTIAL_CONTENT,
                            headers=headers)
        else:
            return Response(
                {'message': "Vous n'êtes pas authorisé a modifier ce projet"},
                status=status.HTTP_403_FORBIDDEN
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.author_user_id == user:
            self.perform_destroy(instance)
            return Response({'message': 'Le projet a bien été supprimer'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Action interdite'},
                            status=status.HTTP_403_FORBIDDEN)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Issue.objects.filter(project_id=project_id)
        return queryset

    '''def create(self, request, *args, **kwargs):
        pass'''


class CommentViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

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