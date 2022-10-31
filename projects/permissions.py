"""
permission class
    return the authentication status for user

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
