from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

class AppointmentStatus(models.TextChoices):
    PENDING = 'pending', _('Pendente')
    CONFIRMED = 'confirmed', _('Confirmado')
    CANCELLED = 'cancelled', _('Cancelado')

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nome'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=255, verbose_name=_('Telefone'))
    date = models.DateField(verbose_name=_('Data'))
    start_time = models.TimeField(unique_for_date='date', verbose_name=_('Hora de início'))
    end_time = models.TimeField(unique_for_date='date', verbose_name=_('Hora de término'))
    message = models.TextField(verbose_name=_('Mensagem'))
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING, verbose_name=_('Status'))

    def __str__(self):
        return self.name
    
