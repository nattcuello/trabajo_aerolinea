from django.urls import path
from . import views

urlpatterns = [
    path('', views.vuelo_list, name='vuelo_list'),
    path('<int:vuelo_id>/', views.vuelo_detail, name='vuelo_detail'),
]
