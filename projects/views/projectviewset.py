"""
Project viewset class

    @get_queryset : returning projects where user is contributor
    @perform_create : create Project and contributors object including
                        the author user POST method
    @update : update the project by its ID PUT method
    @destroy : delete the project by its ID DELETE method

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from projects.permissions import IsAuthenticated

from projects.models.project import Project
from projects.models.contributor import Contributor

from .multipleserializermixin import MultipleSerializerMixin

from projects.serializers.projectlistserializer import ProjectListSerializer
from projects.serializers.projectdetailserializer import \
    ProjectDetailSerializer


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
        if Project.objects.filter(id=self.kwargs['pk']):
            instance = self.get_object()

            serializer = self.get_serializer(instance,
                                             data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            if instance.author_user_id == self.request.user:

                instance = serializer.save()
                self.perform_update(instance)
                headers = self.get_success_headers(serializer.validated_data)
                return Response(serializer.data,
                                status=status.HTTP_200_OK,
                                headers=headers)
            else:
                return Response(
                    {'message': "You are not authorized to modifiy "
                                "this project"},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'message': "This project id doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        if Project.objects.filter(id=self.kwargs['pk']):
            instance = self.get_object()
            user = request.user
            if instance.author_user_id == user:
                self.perform_destroy(instance)
                return Response({'message': 'The project has been deleted'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': "You are not authorized "
                                            "to delete this project"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(
                {'message': "This project id doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
