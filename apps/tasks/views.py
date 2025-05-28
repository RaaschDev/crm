from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm
from apps.department.models import Department
import json

# Create your views here.

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = '/tasks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        form.instance.enterprise = self.request.user.enterprise
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = '/tasks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context

def kanban_board(request):
    todo_tasks = Task.objects.filter(status='todo')
    in_progress_tasks = Task.objects.filter(status='in_progress')
    review_tasks = Task.objects.filter(status='review')
    done_tasks = Task.objects.filter(status='done')
    
    return render(request, 'tasks/kanban.html', {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'review_tasks': review_tasks,
        'done_tasks': done_tasks,
    })

def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        data = json.loads(request.body)
        task.status = data.get('status')
        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=400)
