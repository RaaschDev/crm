from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from .forms import CustomUserForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'pages/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
                    return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserForm()
    
    return render(request, 'pages/register.html', {'form': form})

def logout_view(request):
    """
    View for handling user logout.
    """
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('accounts:login')
