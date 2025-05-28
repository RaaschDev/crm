from django.db import models
from django.contrib.auth import get_user_model
from apps.enterprise.models import Enterprise
from apps.department.models import Department
from utils.models import BaseModel

User = get_user_model()

class Task(BaseModel):
    STATUS_CHOICES = [
        ('todo', 'A Fazer'),
        ('in_progress', 'Em Progresso'),
        ('review', 'Em Revisão'),
        ('done', 'Concluído'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'Alta'),
        ('medium', 'Média'),
        ('low', 'Baixa'),
    ]

    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name="Empresa")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Departamento")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name="Status")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridade")
    due_date = models.DateField(verbose_name="Data de Entrega")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', verbose_name="Atribuído para")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks', verbose_name="Atribuído por")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"


        # 7502ED3B508C-48D8-B1A9-EA3369F2BC6F