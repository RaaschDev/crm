from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Department
from apps.enterprise.models import Enterprise
from apps.employers.models import Employer
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

# Create your views here.

@login_required
def department_list(request):
    print("View department_list chamada")
    if not request.user.enterprise:
        messages.error(request, 'Você precisa estar associado a uma empresa para gerenciar departamentos.')
        return redirect('dashboard:home')
    
    # Annotate departments with employee count
    departments = Department.objects.filter(enterprise=request.user.enterprise)\
        .annotate(employee_count=Count('employer'))\
        .order_by('name')
    
    return render(request, 'department/pages/list.html', {'departments': departments})

@login_required
def department_create(request):
    if not request.user.enterprise:
        messages.error(request, 'Você precisa estar associado a uma empresa para criar departamentos.')
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        leader_id = request.POST.get('leader')
        is_active = request.POST.get('is_active') == 'on'

        try:
            leader = User.objects.get(id=leader_id) if leader_id else None

            department = Department.objects.create(
                name=name,
                description=description,
                leader=leader,
                enterprise=request.user.enterprise,
                is_active=is_active
            )
            messages.success(request, 'Departamento criado com sucesso!')
            return redirect('department:list')
        except Exception as e:
            messages.error(request, f'Erro ao criar departamento: {str(e)}')
    
    leaders = User.objects.filter(enterprise=request.user.enterprise)
    return render(request, 'department/pages/form.html', {
        'leaders': leaders
    })

@login_required
def department_edit(request, pk):
    if not request.user.enterprise:
        messages.error(request, 'Você precisa estar associado a uma empresa para editar departamentos.')
        return redirect('dashboard:home')
        
    department = get_object_or_404(Department, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        leader_id = request.POST.get('leader')
        is_active = request.POST.get('is_active') == 'on'

        try:
            leader = User.objects.get(id=leader_id) if leader_id else None

            department.name = name
            department.description = description
            department.leader = leader
            department.is_active = is_active
            department.save()

            messages.success(request, 'Departamento atualizado com sucesso!')
            return redirect('department:list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar departamento: {str(e)}')
    
    leaders = User.objects.filter(enterprise=request.user.enterprise)
    return render(request, 'department/pages/form.html', {
        'department': department,
        'leaders': leaders
    })

@login_required
def department_delete(request, pk):
    if not request.user.enterprise:
        messages.error(request, 'Você precisa estar associado a uma empresa para excluir departamentos.')
        return redirect('dashboard:home')
        
    department = get_object_or_404(Department, pk=pk, enterprise=request.user.enterprise)
    
    if request.method == 'POST':
        try:
            department.delete()
            messages.success(request, 'Departamento excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir departamento: {str(e)}')
        return redirect('department:list')
    
    return render(request, 'department/pages/delete.html', {'department': department})
