from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clients.models import Client

@login_required
def home(request):
    """
    View for the dashboard home page.
    """
    # Get the user's enterprise
    enterprise = request.user.enterprise
    
    # Count clients for the enterprise
    total_clientes = Client.objects.filter(enterprise=enterprise).count()
    
    context = {
        'total_clientes': total_clientes,
        'tarefas_pendentes': 0,  # TODO: Implement actual count
        'projetos_ativos': 0,  # TODO: Implement actual count
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
