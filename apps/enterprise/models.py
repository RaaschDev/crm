from django.db import models
from utils.models import BaseModel
# Create your models here.

class Enterprise(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')
    logo = models.ImageField(upload_to='enterprise/logo', null=True, blank=True, verbose_name='Logo')
    address = models.CharField(max_length=255, verbose_name='Endereço')
    phone = models.CharField(max_length=255, verbose_name='Telefone')
    email = models.EmailField(max_length=255, verbose_name='Email')
    website = models.URLField(max_length=255, verbose_name='Website')
    
    def __str__(self):
        return self.name
    
    
