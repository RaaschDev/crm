from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('tarefas/', views.tarefas, name='tarefas'),
    path('projetos/', views.projetos, name='projetos'),
]
