from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment, AppointmentStatus
from datetime import datetime, timedelta
import calendar
import json

def fullcalendar_view(request):
    return render(request, 'appointment/fullcalendar.html')

def get_appointments(request):
    # Obter parâmetros de data do FullCalendar
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    try:
        # Converter as datas para o formato correto
        start_date = datetime.fromisoformat(start.replace('Z', '+00:00')).date()
        end_date = datetime.fromisoformat(end.replace('Z', '+00:00')).date()
    except (ValueError, AttributeError):
        # Se não houver datas específicas, retorna eventos do mês atual
        today = timezone.now()
        start_date = today.replace(day=1).date()
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1).date() - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1).date() - timedelta(days=1)

    # Buscar agendamentos no período
    appointments = Appointment.objects.filter(
        date__range=[start_date, end_date],
        status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]
    )

    # Formatar eventos para o FullCalendar
    events = []
    for apt in appointments:
        # Criar datetime combinando data e hora
        start_datetime = datetime.combine(apt.date, apt.start_time)
        end_datetime = datetime.combine(apt.date, apt.end_time)
        
        # Definir cor baseada no status
        color = '#10B981' if apt.status == AppointmentStatus.CONFIRMED else '#F59E0B'
        
        event = {
            'id': str(apt.id),
            'title': f"{apt.name} - {apt.start_time.strftime('%H:%M')}",
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
            'color': color,
            'extendedProps': {
                'email': apt.email,
                'phone': apt.phone,
                'message': apt.message,
                'status': apt.status
            }
        }
        events.append(event)

    return JsonResponse(events, safe=False)

def calendar_view(request):
    # Get current date or use the date from request
    current_date = request.GET.get('date')
    if current_date:
        try:
            current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
        except ValueError:
            current_date = timezone.now().date()
    else:
        current_date = timezone.now().date()

    # Get appointments for the current month
    start_of_month = current_date.replace(day=1)
    if current_date.month == 12:
        end_of_month = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)

    appointments = Appointment.objects.filter(
        date__range=[start_of_month, end_of_month],
        status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]
    )

    # Create calendar data
    cal = calendar.monthcalendar(current_date.year, current_date.month)
    
    # Prepare appointments data for the template
    appointments_data = {}
    for appointment in appointments:
        date_str = appointment.date.strftime('%Y-%m-%d')
        if date_str not in appointments_data:
            appointments_data[date_str] = []
        appointments_data[date_str].append({
            'start_time': appointment.start_time.strftime('%H:%M'),
            'end_time': appointment.end_time.strftime('%H:%M'),
            'name': appointment.name,
            'status': appointment.status
        })

    context = {
        'calendar': cal,
        'current_date': current_date,
        'appointments': appointments_data,
        'month_name': current_date.strftime('%B %Y'),
        'prev_month': (current_date.replace(day=1) - timedelta(days=1)).strftime('%Y-%m-%d'),
        'next_month': (current_date.replace(day=28) + timedelta(days=4)).replace(day=1).strftime('%Y-%m-%d'),
    }
    
    return render(request, 'appointment/calendar.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def create_appointment(request):
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Obter e validar os dados do formulário
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        date_str = data.get('date')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        message = data.get('message', '')

        if not all([name, email, phone, date_str, start_time_str, end_time_str]):
            return JsonResponse({
                'status': 'error',
                'message': 'Todos os campos obrigatórios devem ser preenchidos.'
            }, status=400)

        # Converter strings para objetos date/time
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Formato de data ou hora inválido.'
            }, status=400)

        # Verificar se o horário está disponível
        if Appointment.objects.filter(
            date=date,
            start_time=start_time,
            end_time=end_time,
            status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]
        ).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Este horário já está reservado.'
            }, status=400)

        # Criar o agendamento
        appointment = Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            start_time=start_time,
            end_time=end_time,
            message=message,
            status=AppointmentStatus.PENDING
        )

        # Preparar resposta
        start_datetime = datetime.combine(appointment.date, appointment.start_time)
        end_datetime = datetime.combine(appointment.date, appointment.end_time)

        response_data = {
            'status': 'success',
            'message': 'Agendamento criado com sucesso!',
            'appointment': {
                'id': str(appointment.id),
                'name': appointment.name,
                'date': appointment.date.strftime('%Y-%m-%d'),
                'start_time': appointment.start_time.strftime('%H:%M'),
                'end_time': appointment.end_time.strftime('%H:%M'),
                'email': appointment.email,
                'phone': appointment.phone,
                'message': appointment.message,
                'status': appointment.status
            }
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Dados inválidos. Por favor, envie os dados em formato JSON.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao criar agendamento: {str(e)}'
        }, status=500)
