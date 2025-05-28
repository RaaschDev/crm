from django.db import models
from utils.models.base_model import BaseModel
from apps.enterprise.models import Enterprise
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Líder', blank=True, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name='Empresa')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['name']

    def __str__(self):
        return self.name

