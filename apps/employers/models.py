from django.db import models
from django.contrib.auth import get_user_model
from apps.department.models import Department
from apps.enterprise.models import Enterprise
from utils.models import BaseModel

User = get_user_model()

# Create your models here.

class Employer(BaseModel):
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Telefone', max_length=20)
    position = models.CharField('Cargo', max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Departamento', null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name='Empresa')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['name']

    def __str__(self):
        return self.name
