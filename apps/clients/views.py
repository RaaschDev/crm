from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client

# Create your views here.

@login_required
def client_list(request):
    clients = Client.objects.filter(enterprise=request.user.enterprise).order_by('name')
    return render(request, 'pages/list.html', {'clients': clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        notes = request.POST.get('notes')
        address = request.POST.get('address')

        client = Client.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            notes=notes,
            address=address,
            enterprise=request.user.enterprise
        )
        messages.success(request, 'Cliente criado com sucesso!')
        return redirect('clients:list')

    return render(request, 'pages/form.html')

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk, enterprise=request.user.enterprise)

    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.company = request.POST.get('company')
        client.notes = request.POST.get('notes')
        client.address = request.POST.get('address')
        client.save()

        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('clients:list')

    return render(request, 'pages/form.html', {'client': client})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('clients:list')

    return redirect('clients:list')
