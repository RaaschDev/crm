from django.contrib import admin
from .models import BillingPayable, BillingReceivable, Installment

@admin.register(BillingPayable)
class BillingPayableAdmin(admin.ModelAdmin):
    list_display = ('description', 'supplier', 'total_value', 'installment_count', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('description', 'supplier__name')

@admin.register(BillingReceivable)
class BillingReceivableAdmin(admin.ModelAdmin):
    list_display = ('description', 'client', 'total_value', 'installment_count', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('description', 'client__name')

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'value', 'due_date', 'status', 'paid_at')
    list_filter = ('status', 'due_date')
    search_fields = ('billing_payable__description', 'billing_receivable__description')
