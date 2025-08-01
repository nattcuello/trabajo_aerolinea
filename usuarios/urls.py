from django.urls import path
from .views import registro_usuario
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

# Vista personalizada de logout
class CustomLogoutView(View):
    def post(self, request):
        from django.contrib.auth import logout
        logout(request)
        messages.success(request, "Sesión cerrada correctamente.")
        return redirect('home:index')

app_name = 'usuarios'

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  
]
