from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Chat
from .services import ChatService

# Create your views here.

@login_required
def chat_view(request):
    """View para a página do chat"""
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'chat/pages/chat.html', {'chats': chats})

@login_required
def send_message(request):
    """View para processar mensagens do chat"""
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            chat_service = ChatService()
            response = chat_service.get_response(message)
            
            # Salva a interação no banco de dados
            chat = Chat.objects.create(
                user=request.user,
                message=message,
                response=response
            )
            
            return JsonResponse({
                'status': 'success',
                'response': response,
                'timestamp': chat.created_at.strftime('%d/%m/%Y %H:%M')
            })
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=400)

@login_required
def clear_chat(request):
    """View para limpar o histórico do chat"""
    if request.method == 'POST':
        Chat.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=400)
