from django.db import models
from utils.models.base_model import BaseModel
from apps.enterprise.models import Enterprise

class SupplierTag(BaseModel):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name='Empresa')
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    color = models.CharField(max_length=10, verbose_name='Cor')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')

class Supplier(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='Empresa')
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name='CNPJ')
    address = models.CharField(max_length=255, verbose_name='Endereço')
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name='Empresa')
    tags = models.ManyToManyField(SupplierTag, blank=True, verbose_name='Tags')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['name']

    def __str__(self):
        return self.name
