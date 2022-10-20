from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
            return bool(request.user
                        and request.user.is_authenticated)


class IsAuthor(BasePermission):

    message = "..."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "POST":
            return True
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(...)  # idem que ci dessous, sinon bloquant

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(...)
        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(...)  # "ci dessous", c'est ici
