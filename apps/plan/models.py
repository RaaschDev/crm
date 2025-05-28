from django.db import models
from utils.models import BaseModel
# Create your models here.

class Plan(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    duration = models.IntegerField(verbose_name='Duração')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return self.name
