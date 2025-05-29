from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.suppliers.models import Supplier, SupplierTag
from apps.billings.models import BillingPayable, BillingReceivable, Installment
from apps.enterprise.models import Enterprise
from apps.clients.models import Client
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

class Command(BaseCommand):
    help = 'Gera dados aleatórios para teste'

    def handle(self, *args, **kwargs):
        # Criar tags de fornecedor
        tags = [
            ('Fornecedor de Matéria Prima', '#FF5733'),
            ('Fornecedor de Serviços', '#33FF57'),
            ('Fornecedor de Equipamentos', '#3357FF'),
            ('Fornecedor de TI', '#F333FF'),
            ('Fornecedor de Logística', '#33FFF3'),
        ]

        for name, color in tags:
            SupplierTag.objects.get_or_create(
                name=name,
                defaults={
                    'color': color,
                    'description': f'Tag para {name.lower()}'
                }
            )

        # Pegar a primeira empresa do sistema
        enterprise = Enterprise.objects.first()
        if not enterprise:
            self.stdout.write(self.style.ERROR('Nenhuma empresa encontrada. Crie uma empresa primeiro.'))
            return

        # Criar 30 fornecedores
        suppliers = []
        for _ in range(30):
            company_name = fake.company()
            supplier = Supplier.objects.create(
                enterprise=enterprise,
                name=company_name,
                email=fake.company_email(),
                phone=fake.phone_number(),
                address=fake.address(),
                cnpj=fake.cnpj(),
                company=company_name,
                notes=fake.text(max_nb_chars=200),
                is_active=True
            )
            
            # Adicionar tags aleatórias
            tags = SupplierTag.objects.all()
            supplier.tags.add(*random.sample(list(tags), random.randint(1, 3)))
            
            suppliers.append(supplier)
            self.stdout.write(f'Fornecedor criado: {supplier.name}')

        # Criar contas a pagar
        for _ in range(20):
            supplier = random.choice(suppliers)
            total_value = round(random.uniform(1000, 10000), 2)
            installment_count = random.randint(1, 12)
            installment_value = round(total_value / installment_count, 2)
            due_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
            
            billing = BillingPayable.objects.create(
                enterprise=enterprise,
                supplier=supplier,
                description=fake.text(max_nb_chars=100),
                total_value=total_value,
                installment_count=installment_count,
                installment_value=installment_value,
                due_date=due_date,
                status='pending'
            )
            
            # Criar parcelas
            parcel_due_date = due_date
            for i in range(installment_count):
                Installment.objects.create(
                    billing_payable=billing,
                    number=i + 1,
                    value=installment_value,
                    due_date=parcel_due_date,
                    status='pending'
                )
                parcel_due_date += timedelta(days=30)
            
            self.stdout.write(f'Conta a pagar criada: {billing.description}')

        # Criar contas a receber
        for _ in range(15):
            total_value = round(random.uniform(1000, 10000), 2)
            installment_count = random.randint(1, 12)
            installment_value = round(total_value / installment_count, 2)
            due_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
            
            billing = BillingReceivable.objects.create(
                enterprise=enterprise,
                client=Client.objects.first(),  # Usar o primeiro cliente disponível
                description=fake.text(max_nb_chars=100),
                total_value=total_value,
                installment_count=installment_count,
                installment_value=installment_value,
                due_date=due_date,
                status='pending'
            )
            
            # Criar parcelas
            parcel_due_date = due_date
            for i in range(installment_count):
                Installment.objects.create(
                    billing_receivable=billing,
                    number=i + 1,
                    value=installment_value,
                    due_date=parcel_due_date,
                    status='pending'
                )
                parcel_due_date += timedelta(days=30)
            
            self.stdout.write(f'Conta a receber criada: {billing.description}')

        self.stdout.write(self.style.SUCCESS('Dados de teste gerados com sucesso!')) 