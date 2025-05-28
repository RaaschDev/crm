from django import forms
from .models import Employer
from apps.department.models import Department
from apps.enterprise.models import Enterprise
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployerForm(forms.ModelForm):
    enterprise = forms.ModelChoiceField(
        queryset=Enterprise.objects.all(),
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and hasattr(self.user, 'enterprise'):
            enterprise = self.user.enterprise
            self.fields['department'].queryset = Department.objects.filter(enterprise=enterprise)
            self.fields['user'].queryset = User.objects.filter(enterprise=enterprise)
            self.fields['enterprise'].initial = enterprise

        # Add required field validation
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['position'].required = True
        self.fields['department'].required = True
        self.fields['user'].required = True

        # Add custom error messages
        self.fields['name'].error_messages = {
            'required': 'O nome é obrigatório.',
        }
        self.fields['email'].error_messages = {
            'required': 'O email é obrigatório.',
            'invalid': 'Digite um email válido.',
        }
        self.fields['phone'].error_messages = {
            'required': 'O telefone é obrigatório.',
        }
        self.fields['position'].error_messages = {
            'required': 'O cargo é obrigatório.',
        }
        self.fields['department'].error_messages = {
            'required': 'O departamento é obrigatório.',
        }
        self.fields['user'].error_messages = {
            'required': 'O usuário é obrigatório.',
        }

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        enterprise = cleaned_data.get('enterprise')

        if user and enterprise and user.enterprise != enterprise:
            raise forms.ValidationError('O usuário selecionado não pertence à empresa.')

        return cleaned_data

    class Meta:
        model = Employer
        fields = ['name', 'email', 'phone', 'position', 'department', 'user', 'enterprise', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-blue-800 focus:border-blue-800 block w-full sm:text-sm border-gray-300 rounded-md',
                'style': 'height: 40px; padding-left: 4px; padding-right: 4px; border: 1px solid #D1D5DB;'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'shadow-sm focus:ring-blue-800 focus:border-blue-800 block w-full sm:text-sm border-gray-300 rounded-md',
                'style': 'height: 40px; padding-left: 4px; padding-right: 4px; border: 1px solid #D1D5DB;'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-blue-800 focus:border-blue-800 block w-full sm:text-sm border-gray-300 rounded-md',
                'style': 'height: 40px; padding-left: 4px; padding-right: 4px; border: 1px solid #D1D5DB;'
            }),
            'position': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-blue-800 focus:border-blue-800 block w-full sm:text-sm border-gray-300 rounded-md',
                'style': 'height: 40px; padding-left: 4px; padding-right: 4px; border: 1px solid #D1D5DB;'
            }),
            'department': forms.Select(attrs={
                'class': 'shadow-sm focus:ring-blue-800 focus:border-blue-800 block w-full sm:text-sm border-gray-300 rounded-md',
                'style': 'height: 40px; padding-left: 4px; padding-right: 4px; border: 1px solid #D1D5DB;'
            }),
            'user': forms.Select(attrs={
                'class': 'shadow-sm focus:ring-blue-800 focus:border-blue-800 block w-full sm:text-sm border-gray-300 rounded-md',
                'style': 'height: 40px; padding-left: 4px; padding-right: 4px; border: 1px solid #D1D5DB;'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-800 focus:ring-blue-800 border-gray-300 rounded'
            })
        } 