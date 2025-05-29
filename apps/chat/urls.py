from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('process_message/', views.process_message, name='process_message'),
    path('clear/', views.clear_chat, name='clear_chat'),
] 