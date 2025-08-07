from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm, PerfilUsuarioForm

def registro_usuario(request):
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)  # Hashear la contraseña
            user.save()

            # Solo crear perfil si no existe para este usuario
            if not hasattr(user, 'perfil') or user.perfil is None:
                perfil = perfil_form.save(commit=False)
                perfil.user = user
                perfil.save()

            return redirect('home:index')
    else:
        user_form = UsuarioForm()
        perfil_form = PerfilUsuarioForm()

    return render(request, 'usuarios/registro.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
    })

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def dashboard(request):
    perfil = getattr(request.user, 'perfilusuario', None)
    if perfil and perfil.rol == 'admin':
        # Mostrar vista admin
        return render(request, 'dashboard/admin.html')
    elif perfil and perfil.rol == 'operador':
        # Mostrar vista operador
        return render(request, 'dashboard/operador.html')
    else:
        # Vista para pasajero u otro rol
        return render(request, 'dashboard/user.html')
