from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Supplier, SupplierTag

# Create your views here.

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.filter(enterprise=request.user.enterprise).order_by('name')
    tags = SupplierTag.objects.filter(is_active=True, enterprise=request.user.enterprise).order_by('name')
    
    # Filter by tags if selected
    selected_tags = request.GET.getlist('tags')
    if selected_tags:
        suppliers = suppliers.filter(tags__id__in=selected_tags).distinct()
    
    return render(request, 'suppliers/pages/list.html', {
        'suppliers': suppliers,
        'tags': tags
    })

@login_required
def supplier_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        cnpj = request.POST.get('cnpj')
        address = request.POST.get('address')
        notes = request.POST.get('notes')
        tag_ids = request.POST.getlist('tags')

        supplier = Supplier.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            cnpj=cnpj,
            address=address,
            notes=notes,
            enterprise=request.user.enterprise
        )
        
        # Add tags if selected
        if tag_ids:
            supplier.tags.set(tag_ids)
            
        messages.success(request, 'Fornecedor criado com sucesso!')
        return redirect('suppliers:list')

    tags = SupplierTag.objects.filter(is_active=True).order_by('name')
    return render(request, 'suppliers/pages/form.html', {'tags': tags})

@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, enterprise=request.user.enterprise)

    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.email = request.POST.get('email')
        supplier.phone = request.POST.get('phone')
        supplier.company = request.POST.get('company')
        supplier.cnpj = request.POST.get('cnpj')
        supplier.address = request.POST.get('address')
        supplier.notes = request.POST.get('notes')
        supplier.save()

        # Update tags
        tag_ids = request.POST.getlist('tags')
        supplier.tags.set(tag_ids)

        messages.success(request, 'Fornecedor atualizado com sucesso!')
        return redirect('suppliers:list')

    tags = SupplierTag.objects.filter(is_active=True).order_by('name')
    return render(request, 'suppliers/pages/form.html', {
        'supplier': supplier,
        'tags': tags
    })

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Fornecedor excluído com sucesso!')
        return redirect('suppliers:list')

    return redirect('suppliers:list')

# Tag Views
@login_required
def tag_list(request):
    tags = SupplierTag.objects.filter(is_active=True, enterprise=request.user.enterprise).order_by('name')
    return render(request, 'suppliers/pages/tag_list.html', {'tags': tags})

@login_required
def tag_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        color = request.POST.get('color')

        SupplierTag.objects.create(
            name=name,
            description=description,
            color=color
        )
            
        messages.success(request, 'Tag criada com sucesso!')
        return redirect('suppliers:tag_list')

    return render(request, 'suppliers/pages/tag_form.html')

@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(SupplierTag, pk=pk)

    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.description = request.POST.get('description')
        tag.color = request.POST.get('color')
        tag.save()

        messages.success(request, 'Tag atualizada com sucesso!')
        return redirect('suppliers:tag_list')

    return render(request, 'suppliers/pages/tag_form.html', {'tag': tag})

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(SupplierTag, pk=pk)
    
    if request.method == 'POST':
        tag.is_active = False
        tag.save()
        messages.success(request, 'Tag excluída com sucesso!')
        return redirect('suppliers:tag_list')

    return redirect('suppliers:tag_list')
