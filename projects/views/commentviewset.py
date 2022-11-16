"""
Comment viewset class

    @get_queryset : returning comment by its issue.project_ID
    @perform_create : create Comment object including
                        the author user POST method
    @update : update the comment by its ID PUT method
    @destroy : delete the comment by its ID DELETE method

@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied

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
        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)
            issue_id = self.kwargs['issue_id']
            queryset = Comment.objects.filter(issue_id=issue_id)
            if Contributor.objects.filter(project_id=project_id,
                                          user_id=self.request.user).exists():
                if Issue.objects.filter(id=issue_id).exists():
                    issue = Issue.objects.get(id=issue_id)
                    if issue.project_id == project:
                        return queryset
                    else:
                        raise ValidationError(detail="This issue doesn't "
                                                     "exists for this project")
                else:
                    raise ValidationError(detail="This issue doesn't exists")
            else:
                raise PermissionDenied(detail="You are not contributor "
                                              "for this project")
        else:
            raise ValidationError(detail="This project doesn't exists")

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        issue_id = self.kwargs['issue_id']
        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)
            if Issue.objects.filter(id=issue_id).exists():
                issue = Issue.objects.get(id=issue_id)
                if issue.project_id == project:
                    if Contributor.objects.filter(project_id=project.id,
                                                  user_id=self.request.user
                                                  ).exists():
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
                    else:
                        return Response({'message': "You are not contributor "
                                                    "for this project"},
                                        status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'message': "This issue doesn't exists "
                                                "for this project"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "This issue doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "This project doesn't exists"},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        issue_id = self.kwargs['issue_id']
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)
            if Issue.objects.filter(id=issue_id).exists():
                issue = Issue.objects.get(id=issue_id)
                if issue.project_id == project:
                    if instance.issue_id == issue:
                        if instance.author_user_id.id == self.request.user.id:
                            instance = serializer.save()
                            self.perform_update(instance)
                            headers = self.get_success_headers(
                                serializer.validated_data)
                            return Response(serializer.data,
                                            status=status.HTTP_200_OK,
                                            headers=headers)
                        else:
                            return Response(
                                {'message': "You are not the comment's "
                                            "author"},
                                status=status.HTTP_403_FORBIDDEN
                            )
                    else:
                        return Response(
                            {"message": "This comment doesn't exists for "
                                        "this issue"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'message': "This issue doesn't exists "
                                    "for this project"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "This issue doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "This project doesn't exists"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        issue_id = self.kwargs['issue_id']
        instance = self.get_object()
        user = request.user
        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)
            if Issue.objects.filter(id=issue_id).exists():
                issue = Issue.objects.get(id=issue_id)
                if issue.project_id == project:
                    if instance.issue_id == issue:
                        if instance.author_user_id == user:
                            self.perform_destroy(instance)
                            return Response(
                                {'message': 'The comment has been deleted'},
                                status=status.HTTP_200_OK)
                        else:
                            return Response({'message': "You are not "
                                                        "authorized to delete "
                                                        "this comment"},
                                            status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response(
                            {"message": "This comment doesn't exists for "
                                        "this issue"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'message': "This issue doesn't exists "
                                    "for this project"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': "This issue doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "This project doesn't exists"},
                            status=status.HTTP_400_BAD_REQUEST)
