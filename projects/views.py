from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponseForbidden

from projects.permissions import IsAuthor, IsAuthenticated
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
            return HttpResponseForbidden(
                "Vous n'êtes pas authorisé a modifier ce projet"
            )


class IssueViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Issue.objects.filter(project_id=project_id)
        return queryset


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


class ContributorViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):

    serializer_class = ContributorSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Contributor.objects.filter(project_id=project_id)
        return queryset
