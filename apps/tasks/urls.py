from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.kanban_board, name='kanban'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='edit'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_status'),
]
