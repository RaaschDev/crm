from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import BillingPayable, BillingReceivable, Installment
from .forms import BillingPayableForm, BillingReceivableForm, SettlementForm
from apps.clients.models import Client
from apps.suppliers.models import Supplier
import csv
from datetime import datetime

# Create your views here.

@login_required
def payable_list(request):
    """Lista todas as contas a pagar"""
    enterprise = request.user.enterprise
    billings = BillingPayable.objects.filter(enterprise=enterprise).order_by('-created_at')
    suppliers = Supplier.objects.filter(enterprise=enterprise, is_active=True)
    
    # Calcular totais
    total_settled = sum(billing.settled_value for billing in billings)
    total_pending = sum(billing.pending_value for billing in billings)
    
    # Exportar para CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="contas_pagar_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Fornecedor', 'Descrição', 'Valor Total', 'Valor Parcela', 'Número de Parcelas', 'Data Vencimento', 'Status', 'Data Criação'])
        
        for billing in billings:
            writer.writerow([
                billing.supplier.name,
                billing.description,
                billing.total_value,
                billing.installment_value,
                billing.installment_count,
                billing.due_date.strftime('%d/%m/%Y'),
                billing.get_status_display(),
                billing.created_at.strftime('%d/%m/%Y %H:%M')
            ])
        
        return response
    
    context = {
        'billings': billings,
        'suppliers': suppliers,
        'total_settled': total_settled,
        'total_pending': total_pending,
    }
    return render(request, 'billings/pages/payable_list.html', context)

@login_required
def payable_create(request):
    if request.method == 'POST':
        form = BillingPayableForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.enterprise = request.user.enterprise
            billing.save()

            # Criar parcelas
            for i in range(billing.installment_count):
                Installment.objects.create(
                    billing_payable=billing,
                    number=i + 1,
                    value=billing.installment_value,
                    due_date=billing.due_date
                )

            messages.success(request, 'Conta a pagar criada com sucesso!')
            return redirect('billings:payable_list')
    else:
        form = BillingPayableForm()
        form.fields['supplier'].queryset = Supplier.objects.filter(enterprise=request.user.enterprise, is_active=True)

    return render(request, 'billings/pages/payable_form.html', {
        'form': form,
        'title': 'Nova Conta a Pagar'
    })

@login_required
def payable_edit(request, pk):
    billing = get_object_or_404(BillingPayable, pk=pk, enterprise=request.user.enterprise)

    if request.method == 'POST':
        form = BillingPayableForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta a pagar atualizada com sucesso!')
            return redirect('billings:payable_list')
    else:
        form = BillingPayableForm(instance=billing)
        form.fields['supplier'].queryset = Supplier.objects.filter(enterprise=request.user.enterprise, is_active=True)

    return render(request, 'billings/pages/payable_form.html', {
        'form': form,
        'billing': billing,
        'title': 'Editar Conta a Pagar'
    })

@login_required
def payable_delete(request, pk):
    billing = get_object_or_404(BillingPayable, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        billing.delete()
        messages.success(request, 'Conta a pagar excluída com sucesso!')
        return redirect('billings:payable_list')

    return redirect('billings:payable_list')

@login_required
def receivable_list(request):
    """Lista todas as contas a receber"""
    enterprise = request.user.enterprise
    billings = BillingReceivable.objects.filter(enterprise=enterprise).order_by('-created_at')
    clients = Client.objects.filter(enterprise=enterprise, is_active=True)
    
    # Calcular totais
    total_settled = sum(billing.settled_value for billing in billings)
    total_pending = sum(billing.pending_value for billing in billings)
    
    # Exportar para CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="contas_receber_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Cliente', 'Descrição', 'Valor Total', 'Valor Parcela', 'Número de Parcelas', 'Data Vencimento', 'Status', 'Data Criação'])
        
        for billing in billings:
            writer.writerow([
                billing.client.name,
                billing.description,
                billing.total_value,
                billing.installment_value,
                billing.installment_count,
                billing.due_date.strftime('%d/%m/%Y'),
                billing.get_status_display(),
                billing.created_at.strftime('%d/%m/%Y %H:%M')
            ])
        
        return response
    
    context = {
        'billings': billings,
        'clients': clients,
        'total_settled': total_settled,
        'total_pending': total_pending,
    }
    return render(request, 'billings/pages/receivable_list.html', context)

@login_required
def receivable_create(request):
    if request.method == 'POST':
        form = BillingReceivableForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.enterprise = request.user.enterprise
            billing.save()

            # Criar parcelas
            for i in range(billing.installment_count):
                Installment.objects.create(
                    billing_receivable=billing,
                    number=i + 1,
                    value=billing.installment_value,
                    due_date=billing.due_date
                )

            messages.success(request, 'Conta a receber criada com sucesso!')
            return redirect('billings:receivable_list')
    else:
        form = BillingReceivableForm()
        form.fields['client'].queryset = Client.objects.filter(enterprise=request.user.enterprise, is_active=True)

    return render(request, 'billings/pages/receivable_form.html', {
        'form': form,
        'title': 'Nova Conta a Receber'
    })

@login_required
def receivable_edit(request, pk):
    billing = get_object_or_404(BillingReceivable, pk=pk, enterprise=request.user.enterprise)

    if request.method == 'POST':
        form = BillingReceivableForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta a receber atualizada com sucesso!')
            return redirect('billings:receivable_list')
    else:
        form = BillingReceivableForm(instance=billing)
        form.fields['client'].queryset = Client.objects.filter(enterprise=request.user.enterprise, is_active=True)

    return render(request, 'billings/pages/receivable_form.html', {
        'form': form,
        'billing': billing,
        'title': 'Editar Conta a Receber'
    })

@login_required
def receivable_delete(request, pk):
    billing = get_object_or_404(BillingReceivable, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        billing.delete()
        messages.success(request, 'Conta a receber excluída com sucesso!')
        return redirect('billings:receivable_list')

    return redirect('billings:receivable_list')

@login_required
def installment_pay(request, pk):
    installment = get_object_or_404(Installment, pk=pk)
    
    if request.method == 'POST':
        installment.mark_as_paid()
        messages.success(request, 'Parcela marcada como paga com sucesso!')
        
        # Redirecionar para a lista apropriada
        if installment.billing_payable:
            return redirect('billings:payable_list')
        return redirect('billings:receivable_list')

    return redirect('billings:payable_list')

@login_required
def payable_settle(request, pk):
    billing = get_object_or_404(BillingPayable, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        form = SettlementForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            date = form.cleaned_data['date']
            
            if value > billing.pending_value:
                messages.error(request, 'O valor informado é maior que o valor pendente.')
            else:
                billing.settle(value, date)
                messages.success(request, 'Conta liquidada com sucesso!')
                return redirect('billings:payable_list')
    else:
        form = SettlementForm(initial={'date': datetime.now().date()})
    
    return render(request, 'billings/pages/settlement_form.html', {
        'form': form,
        'billing': billing,
        'title': 'Liquidar Conta a Pagar'
    })

@login_required
def receivable_settle(request, pk):
    billing = get_object_or_404(BillingReceivable, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        form = SettlementForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            date = form.cleaned_data['date']
            
            if value > billing.pending_value:
                messages.error(request, 'O valor informado é maior que o valor pendente.')
            else:
                billing.settle(value, date)
                messages.success(request, 'Conta liquidada com sucesso!')
                return redirect('billings:receivable_list')
    else:
        form = SettlementForm(initial={'date': datetime.now().date()})
    
    return render(request, 'billings/pages/settlement_form.html', {
        'form': form,
        'billing': billing,
        'title': 'Liquidar Conta a Receber'
    })
