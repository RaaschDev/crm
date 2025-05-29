from django.db import models
from utils.models.base_model import BaseModel
from apps.enterprise.models import Enterprise
from django.utils import timezone
from apps.suppliers.models import Supplier
from apps.clients.models import Client


class BillingPayable(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('overdue', 'Atrasado'),
        ('settled', 'Liquidado'),
    ]

    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    installment_count = models.PositiveIntegerField(default=1)
    installment_value = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    settlement_date = models.DateField(null=True, blank=True)
    settled_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.supplier.name} - {self.description}"

    def save(self, *args, **kwargs):
        if not self.pending_value:
            self.pending_value = self.total_value
        super().save(*args, **kwargs)

    def update_status(self):
        if self.status == 'settled':
            return

        if self.settlement_date and self.settled_value >= self.total_value:
            self.status = 'settled'
        elif self.due_date < timezone.now().date() and self.status != 'paid':
            self.status = 'overdue'
        elif self.settled_value > 0:
            self.status = 'paid'
        else:
            self.status = 'pending'
        
        self.pending_value = self.total_value - self.settled_value
        self.save()

    def settle(self, value, date=None):
        if not date:
            date = timezone.now().date()
        
        self.settled_value += value
        self.settlement_date = date
        self.update_status()

    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status == 'pending'

class BillingReceivable(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('overdue', 'Atrasado'),
        ('settled', 'Liquidado'),
    ]

    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    installment_count = models.PositiveIntegerField(default=1)
    installment_value = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    settlement_date = models.DateField(null=True, blank=True)
    settled_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.client.name} - {self.description}"

    def save(self, *args, **kwargs):
        if not self.pending_value:
            self.pending_value = self.total_value
        super().save(*args, **kwargs)

    def update_status(self):
        if self.status == 'settled':
            return

        if self.settlement_date and self.settled_value >= self.total_value:
            self.status = 'settled'
        elif self.due_date < timezone.now().date() and self.status != 'paid':
            self.status = 'overdue'
        elif self.settled_value > 0:
            self.status = 'paid'
        else:
            self.status = 'pending'
        
        self.pending_value = self.total_value - self.settled_value
        self.save()

    def settle(self, value, date=None):
        if not date:
            date = timezone.now().date()
        
        self.settled_value += value
        self.settlement_date = date
        self.update_status()

    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status == 'pending'

class Installment(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('overdue', 'Atrasado'),
        ('cancelled', 'Cancelado'),
    ]

    billing_payable = models.ForeignKey(BillingPayable, on_delete=models.CASCADE, null=True, blank=True)
    billing_receivable = models.ForeignKey(BillingReceivable, on_delete=models.CASCADE, null=True, blank=True)
    number = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['due_date']

    def __str__(self):
        billing = self.billing_payable or self.billing_receivable
        return f"Parcela {self.number} de {billing}"

    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status == 'pending'

    def mark_as_paid(self):
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()

        # Atualiza o status da conta
        if self.billing_payable:
            self.billing_payable.settle(self.value)
        else:
            self.billing_receivable.settle(self.value)