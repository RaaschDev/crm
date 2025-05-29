from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Client, ClientTag

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
        tags = request.POST.getlist('tags')

        client = Client.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            notes=notes,
            address=address,
            enterprise=request.user.enterprise
        )
        
        if tags:
            client.tags.set(tags)
            
        messages.success(request, 'Cliente criado com sucesso!')
        return redirect('clients:list')

    tags = ClientTag.objects.filter(enterprise=request.user.enterprise, is_active=True)
    return render(request, 'pages/form.html', {'tags': tags})

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

        tags = request.POST.getlist('tags')
        client.tags.set(tags)

        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('clients:list')

    tags = ClientTag.objects.filter(enterprise=request.user.enterprise, is_active=True)
    return render(request, 'pages/form.html', {'client': client, 'tags': tags})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('clients:list')

    return redirect('clients:list')

@login_required
def toggle_client_tag(request, client_id, tag_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, pk=client_id, enterprise=request.user.enterprise)
        tag = get_object_or_404(ClientTag, pk=tag_id, enterprise=request.user.enterprise)
        
        if tag in client.tags.all():
            client.tags.remove(tag)
            added = False
        else:
            client.tags.add(tag)
            added = True
            
        return JsonResponse({
            'success': True,
            'added': added,
            'tag_id': tag_id,
            'tag_name': tag.name,
            'tag_color': tag.color
        })
    
    return JsonResponse({'success': False}, status=400)

@login_required
def tag_list(request):
    tags = ClientTag.objects.filter(enterprise=request.user.enterprise).order_by('name')
    return render(request, 'pages/tag_list.html', {'tags': tags})

@login_required
def tag_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        color = request.POST.get('color')

        tag = ClientTag.objects.create(
            name=name,
            description=description,
            color=color,
            enterprise=request.user.enterprise
        )
        messages.success(request, 'Tag criada com sucesso!')
        return redirect('clients:tag_list')

    return render(request, 'pages/tag_form.html')

@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(ClientTag, pk=pk, enterprise=request.user.enterprise)

    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.description = request.POST.get('description')
        tag.color = request.POST.get('color')
        tag.save()

        messages.success(request, 'Tag atualizada com sucesso!')
        return redirect('clients:tag_list')

    return render(request, 'pages/tag_form.html', {'tag': tag})

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(ClientTag, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag excluída com sucesso!')
        return redirect('clients:tag_list')

    return redirect('clients:tag_list')
