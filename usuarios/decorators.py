from django.shortcuts import redirect
from functools import wraps

def role_required(*roles):
    """
    Decorador que permite el acceso solo a usuarios con alguno de los roles especificados.
    Uso:
        @role_required('admin', 'operador')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('usuarios:login')
            
            # Verificar que tenga el atributo perfil y rol
            if not hasattr(request.user, 'perfil') or request.user.perfil is None:
                return redirect('home:index')

            if request.user.perfil.rol not in roles:
                return redirect('home:index')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
