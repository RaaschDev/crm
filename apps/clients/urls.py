from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='list'),
    path('create/', views.client_create, name='create'),
    path('<int:pk>/edit/', views.client_edit, name='edit'),
    path('<int:pk>/delete/', views.client_delete, name='delete'),
    path('<int:client_id>/tags/<int:tag_id>/toggle/', views.toggle_client_tag, name='toggle_tag'),
    # Tag URLs
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    # Search URLs
    path('search/by-tags/', views.search_clients_by_tags, name='search_by_tags'),
]
