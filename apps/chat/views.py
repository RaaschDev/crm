from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Chat
from .services import ChatService
from apps.reports.utils import (
    generate_billing_report,
    generate_client_report,
    generate_supplier_report,
    generate_pdf
)
from apps.billings.models import BillingPayable, BillingReceivable
from apps.suppliers.models import Supplier
from apps.clients.models import Client
from datetime import datetime
import json
import os
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def chat_view(request):
    """View para a página do chat"""
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'chat/chat.html', {'chats': chats})

@csrf_exempt
@login_required
def process_message(request):
    """Processa a mensagem do usuário e retorna uma resposta"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').lower()
            enterprise = request.user.enterprise

            # Verificar se é uma solicitação de relatório
            if 'relatório' in message or 'relatorio' in message:
                # Relatório de contas a pagar
                if 'contas a pagar' in message or 'contas pagar' in message:
                    billings = BillingPayable.objects.filter(enterprise=enterprise)
                    total_settled = sum(billing.settled_value for billing in billings)
                    total_pending = sum(billing.pending_value for billing in billings)
                    
                    report_data = generate_billing_report(enterprise)
                    report_data['total_settled'] = total_settled
                    report_data['total_pending'] = total_pending
                    
                    filename = f'relatorio_contas_pagar_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                    generate_pdf('reports/billing_report.html', report_data, filename)
                    
                    pdf_url = request.build_absolute_uri('/media/reports/' + filename)
                    response = f'Relatório de contas a pagar gerado com sucesso!\n\nValor Total Liquidado: R$ {total_settled:.2f}\nValor Total Pendente: R$ {total_pending:.2f}\n\nClique aqui para baixar: {pdf_url}'
                    
                    # Salva a interação no banco de dados
                    Chat.objects.create(
                        user=request.user,
                        message=message,
                        response=response
                    )
                    
                    return JsonResponse({
                        'response': response,
                        'pdf_url': pdf_url
                    })
                
                # Relatório de contas a receber
                elif 'contas a receber' in message or 'contas receber' in message:
                    billings = BillingReceivable.objects.filter(enterprise=enterprise)
                    total_settled = sum(billing.settled_value for billing in billings)
                    total_pending = sum(billing.pending_value for billing in billings)
                    
                    report_data = generate_billing_report(enterprise)
                    report_data['total_settled'] = total_settled
                    report_data['total_pending'] = total_pending
                    
                    filename = f'relatorio_contas_receber_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                    generate_pdf('reports/billing_report.html', report_data, filename)
                    
                    pdf_url = request.build_absolute_uri('/media/reports/' + filename)
                    response = f'Relatório de contas a receber gerado com sucesso!\n\nValor Total Liquidado: R$ {total_settled:.2f}\nValor Total Pendente: R$ {total_pending:.2f}\n\nClique aqui para baixar: {pdf_url}'
                    
                    # Salva a interação no banco de dados
                    Chat.objects.create(
                        user=request.user,
                        message=message,
                        response=response
                    )
                    
                    return JsonResponse({
                        'response': response,
                        'pdf_url': pdf_url
                    })
                
                # Relatório de fornecedores
                elif 'fornecedores' in message:
                    report_data = generate_supplier_report(enterprise)
                    filename = f'relatorio_fornecedores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                    generate_pdf('reports/supplier_report.html', report_data, filename)
                    
                    pdf_url = request.build_absolute_uri('/media/reports/' + filename)
                    response = f'Relatório de fornecedores gerado com sucesso!\n\nClique aqui para baixar: {pdf_url}'
                    
                    # Salva a interação no banco de dados
                    Chat.objects.create(
                        user=request.user,
                        message=message,
                        response=response
                    )
                    
                    return JsonResponse({
                        'response': response,
                        'pdf_url': pdf_url
                    })
                
                # Relatório de clientes
                elif 'clientes' in message:
                    report_data = generate_client_report(enterprise)
                    filename = f'relatorio_clientes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
                    generate_pdf('reports/client_report.html', report_data, filename)
                    
                    pdf_url = request.build_absolute_uri('/media/reports/' + filename)
                    response = f'Relatório de clientes gerado com sucesso!\n\nClique aqui para baixar: {pdf_url}'
                    
                    # Salva a interação no banco de dados
                    Chat.objects.create(
                        user=request.user,
                        message=message,
                        response=response
                    )
                    
                    return JsonResponse({
                        'response': response,
                        'pdf_url': pdf_url
                    })
                
                else:
                    response = 'Por favor, especifique qual relatório você deseja gerar:\n- Relatório de contas a pagar\n- Relatório de contas a receber\n- Relatório de fornecedores\n- Relatório de clientes'
                    
                    # Salva a interação no banco de dados
                    Chat.objects.create(
                        user=request.user,
                        message=message,
                        response=response
                    )
                    
                    return JsonResponse({'response': response})
            
            # Se não for uma solicitação de relatório, retorna uma mensagem padrão
            response = 'Olá! Como posso ajudar? Você pode solicitar relatórios de:\n- Contas a pagar\n- Contas a receber\n- Fornecedores\n- Clientes'
            
            # Salva a interação no banco de dados
            Chat.objects.create(
                user=request.user,
                message=message,
                response=response
            )
            
            return JsonResponse({'response': response})
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return JsonResponse({
                'response': 'Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=400)

@login_required
def clear_chat(request):
    """View para limpar o histórico do chat"""
    if request.method == 'POST':
        Chat.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=400)
