from rest_framework.permissions import BasePermission, SAFE_METHODS

def get_user_role(user):
    try:
        return user.perfil.rol
    except Exception:
        return None

class IsAdminOrOperadorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        role = get_user_role(request.user) if request.user and request.user.is_authenticated else None
        return role in ("admin", "operador")