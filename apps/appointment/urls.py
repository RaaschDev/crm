from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('fullcalendar/', views.fullcalendar_view, name='fullcalendar'),
    path('appointments/', views.get_appointments, name='get_appointments'),
    path('create/', views.create_appointment, name='create_appointment'),
] 