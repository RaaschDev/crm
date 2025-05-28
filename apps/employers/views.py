from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employer
from .forms import EmployerForm
from apps.department.models import Department
from apps.enterprise.models import Enterprise
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def employer_list(request):
    try:
        enterprise = request.user.enterprise
        employers = Employer.objects.filter(enterprise=enterprise)
        return render(request, 'employers/pages/list.html', {'employers': employers})
    except AttributeError:
        messages.error(request, 'Você precisa estar vinculado a uma empresa para acessar esta página.')
        return redirect('dashboard:index')

@login_required
def employer_list_by_department(request, department_id):
    try:
        enterprise = request.user.enterprise
        department = get_object_or_404(Department, id=department_id, enterprise=enterprise)
        employers = Employer.objects.filter(department=department, enterprise=enterprise)
        return render(request, 'employers/pages/list.html', {
            'employers': employers,
            'department': department,
            'show_department_filter': False
        })
    except AttributeError:
        messages.error(request, 'Você precisa estar vinculado a uma empresa para acessar esta página.')
        return redirect('dashboard:index')

@login_required
def employer_create(request):
    try:
        enterprise = request.user.enterprise

        if request.method == 'POST':
            form = EmployerForm(request.POST, user=request.user)
            if form.is_valid():
                try:
                    employer = form.save(commit=False)
                    employer.enterprise = enterprise
                    employer.save()
                    messages.success(request, 'Funcionário criado com sucesso!')
                    return redirect('employers:list')
                except Exception as e:
                    messages.error(request, f'Erro ao criar funcionário: {str(e)}')
        else:
            form = EmployerForm(user=request.user)

        return render(request, 'employers/pages/form.html', {'form': form})
    except AttributeError:
        messages.error(request, 'Você precisa estar vinculado a uma empresa para acessar esta página.')
        return redirect('dashboard:index')

@login_required
def employer_edit(request, pk):
    try:
        enterprise = request.user.enterprise
        employer = get_object_or_404(Employer, pk=pk, enterprise=enterprise)

        if request.method == 'POST':
            form = EmployerForm(request.POST, instance=employer, user=request.user)
            if form.is_valid():
                try:
                    employer = form.save(commit=False)
                    employer.enterprise = enterprise
                    employer.save()
                    messages.success(request, 'Funcionário atualizado com sucesso!')
                    return redirect('employers:list')
                except Exception as e:
                    messages.error(request, f'Erro ao atualizar funcionário: {str(e)}')
        else:
            form = EmployerForm(instance=employer, user=request.user)

        return render(request, 'employers/pages/form.html', {
            'form': form,
            'employer': employer
        })
    except AttributeError:
        messages.error(request, 'Você precisa estar vinculado a uma empresa para acessar esta página.')
        return redirect('dashboard:index')

@login_required
def employer_delete(request, pk):
    try:
        enterprise = request.user.enterprise
        employer = get_object_or_404(Employer, pk=pk, enterprise=enterprise)

        if request.method == 'POST':
            try:
                employer.delete()
                messages.success(request, 'Funcionário excluído com sucesso!')
                return redirect('employers:list')
            except Exception as e:
                messages.error(request, f'Erro ao excluir funcionário: {str(e)}')

        return render(request, 'employers/pages/delete.html', {'employer': employer})
    except AttributeError:
        messages.error(request, 'Você precisa estar vinculado a uma empresa para acessar esta página.')
        return redirect('dashboard:index')
