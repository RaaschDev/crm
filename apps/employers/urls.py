from django.urls import path
from . import views

app_name = 'employers'

urlpatterns = [
    path('', views.employer_list, name='list'),
    path('create/', views.employer_create, name='create'),
    path('<int:pk>/edit/', views.employer_edit, name='edit'),
    path('<int:pk>/delete/', views.employer_delete, name='delete'),
    path('department/<int:department_id>/', views.employer_list_by_department, name='list_by_department'),
]
