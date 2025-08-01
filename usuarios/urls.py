from django.urls import path
from .views import registro_usuario
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home:index'), name='logout'),
]
