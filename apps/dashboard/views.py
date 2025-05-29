from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clients.models import Client
from apps.suppliers.models import Supplier
from apps.tasks.models import Task
from apps.billings.models import BillingPayable, BillingReceivable
from django.db.models import Sum

@login_required
def home(request):
    """
    View for the dashboard home page.
    """
    # Get the user's enterprise
    enterprise = request.user.enterprise
    
    # Clientes
    total_clients = Client.objects.filter(enterprise=enterprise, is_active=True).count()
    
    # Fornecedores
    total_suppliers = Supplier.objects.filter(enterprise=enterprise, is_active=True).count()
    
    # Tarefas
    total_tasks = Task.objects.filter(enterprise=enterprise).count()
    pending_tasks = Task.objects.filter(enterprise=enterprise, status='pending').count()
    
    # Contas a Pagar
    total_payable = BillingPayable.objects.filter(
        enterprise=enterprise,
        status='pending'
    ).aggregate(total=Sum('total_value'))['total'] or 0
    
    # Contas a Receber
    total_receivable = BillingReceivable.objects.filter(
        enterprise=enterprise,
        status='pending'
    ).aggregate(total=Sum('total_value'))['total'] or 0
    
    context = {
        'total_clients': total_clients,
        'total_suppliers': total_suppliers,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'total_payable': total_payable,
        'total_receivable': total_receivable,
    }
    return render(request, 'pages/home.html', context)

@login_required
def clientes(request):
    """
    View for the clients page.
    """
    return render(request, 'pages/clientes.html')

@login_required
def tarefas(request):
    """
    View for the tasks page.
    """
    return render(request, 'pages/tarefas.html')

@login_required
def projetos(request):
    """
    View for the projects page.
    """
    return render(request, 'pages/projetos.html')
