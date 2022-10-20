from rest_framework.permissions import BasePermission
from projects.models import Contributor


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user


class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        contributors = Contributor.objects.filter(project_id=obj.id)
        for contributor in contributors:
            if contributor.user_id == request.user:
                return True
        return False
