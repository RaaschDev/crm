from django.db import models
from utils.models.base_model import BaseModel
from apps.enterprise.models import Enterprise
# Create your models here.

class Client(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='Empresa')
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    address = models.CharField(max_length=255, verbose_name='Endereço')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name='Empresa')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']

    def __str__(self):
        return self.name
    