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
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=True)
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
                {'message': "Vous n'êtes pas authorisé à modifier ce projet"},
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
            return Response({'message': "Vous n'êts pas autorisé "
                                        "à supprimer ce projet"},
                            status=status.HTTP_403_FORBIDDEN)
