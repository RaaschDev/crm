from datetime import datetime
from django.db.models import Sum, Count
from apps.billings.models import BillingPayable, BillingReceivable
from apps.clients.models import Client
from apps.suppliers.models import Supplier
from weasyprint import HTML
from django.template.loader import render_to_string
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

def generate_billing_report(enterprise, start_date=None, end_date=None):
    """Generate billing report (payable and receivable)"""
    if not start_date:
        start_date = datetime.now().replace(day=1)
    if not end_date:
        end_date = datetime.now()

    # Contas a Pagar
    payable_data = BillingPayable.objects.filter(
        enterprise=enterprise,
        created_at__range=[start_date, end_date]
    ).values('status').annotate(
        count=Count('id'),
        total=Sum('total_value')
    )

    # Contas a Receber
    receivable_data = BillingReceivable.objects.filter(
        enterprise=enterprise,
        created_at__range=[start_date, end_date]
    ).values('status').annotate(
        count=Count('id'),
        total=Sum('total_value')
    )

    return {
        'payable': payable_data,
        'receivable': receivable_data,
        'start_date': start_date,
        'end_date': end_date
    }

def generate_client_report(enterprise, start_date=None, end_date=None):
    """Generate client report (new and inactive)"""
    if not start_date:
        start_date = datetime.now().replace(day=1)
    if not end_date:
        end_date = datetime.now()

    # Novos clientes
    new_clients = Client.objects.filter(
        enterprise=enterprise,
        created_at__range=[start_date, end_date]
    ).count()

    # Clientes inativos
    inactive_clients = Client.objects.filter(
        enterprise=enterprise,
        is_active=False,
        updated_at__range=[start_date, end_date]
    ).count()

    # Total de clientes
    total_clients = Client.objects.filter(
        enterprise=enterprise
    ).count()

    return {
        'new_clients': new_clients,
        'inactive_clients': inactive_clients,
        'total_clients': total_clients,
        'start_date': start_date,
        'end_date': end_date
    }

def generate_supplier_report(enterprise, start_date=None, end_date=None):
    """Generate supplier report (new and inactive)"""
    if not start_date:
        start_date = datetime.now().replace(day=1)
    if not end_date:
        end_date = datetime.now()

    # Novos fornecedores
    new_suppliers = Supplier.objects.filter(
        enterprise=enterprise,
        created_at__range=[start_date, end_date]
    ).count()

    # Fornecedores inativos
    inactive_suppliers = Supplier.objects.filter(
        enterprise=enterprise,
        is_active=False,
        updated_at__range=[start_date, end_date]
    ).count()

    # Total de fornecedores
    total_suppliers = Supplier.objects.filter(
        enterprise=enterprise
    ).count()

    return {
        'new_suppliers': new_suppliers,
        'inactive_suppliers': inactive_suppliers,
        'total_suppliers': total_suppliers,
        'start_date': start_date,
        'end_date': end_date
    }

def generate_pdf(template_name, context, filename):
    """Generate PDF from template"""
    try:
        logger.info(f"Starting PDF generation for {filename}")
        
        # Render HTML
        logger.info("Rendering HTML template")
        html_string = render_to_string(template_name, context)
        
        # Create PDF
        logger.info("Creating PDF from HTML")
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        # Save PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
        logger.info(f"Saving PDF to {pdf_path}")
        
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf)
        
        logger.info("PDF generated successfully")
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise 