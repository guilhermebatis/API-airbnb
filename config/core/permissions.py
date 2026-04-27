from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin pode tudo
        if request.user.is_staff:
            return True
        # Usuário só pode acessar seus próprios objetos
        return obj.user == request.user
