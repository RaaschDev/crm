from django.urls import path
from . import views

app_name = 'billings'

urlpatterns = [
    # Contas a Pagar
    path('payable/', views.payable_list, name='payable_list'),
    path('payable/create/', views.payable_create, name='payable_create'),
    path('payable/<int:pk>/edit/', views.payable_edit, name='payable_edit'),
    path('payable/<int:pk>/delete/', views.payable_delete, name='payable_delete'),
    path('payable/<int:pk>/settle/', views.payable_settle, name='payable_settle'),
    
    # Contas a Receber
    path('receivable/', views.receivable_list, name='receivable_list'),
    path('receivable/create/', views.receivable_create, name='receivable_create'),
    path('receivable/<int:pk>/edit/', views.receivable_edit, name='receivable_edit'),
    path('receivable/<int:pk>/delete/', views.receivable_delete, name='receivable_delete'),
    path('receivable/<int:pk>/settle/', views.receivable_settle, name='receivable_settle'),
    
    # Parcelas
    path('installment/<int:pk>/pay/', views.installment_pay, name='installment_pay'),
] 