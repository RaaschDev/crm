from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4',
            'type': 'date'
        }),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'department']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4',
                'placeholder': 'Digite o título da tarefa'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4',
                'rows': 3,
                'placeholder': 'Digite a descrição da tarefa'
            }),
            'status': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4'
            }),
            'priority': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4'
            }),
            'department': forms.Select(attrs={
                'class': 'block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-4'
            })
        } 