from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UsuarioForm, PerfilUsuarioForm

def registro_usuario(request):
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)  # importante: guardar password hasheado
            user.save()

            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            return redirect('home:index')  # o a donde quieras redirigir
    else:
        user_form = UsuarioForm()
        perfil_form = PerfilUsuarioForm()

    return render(request, 'usuarios/registro.html', {'user_form': user_form, 'perfil_form': perfil_form})

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

