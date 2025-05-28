from django.core.management.base import BaseCommand
from apps.clients.models import Client
from apps.enterprise.models import Enterprise
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Cria 20 clientes fictícios no sistema'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        
        # Get the first enterprise from the database
        enterprise = Enterprise.objects.first()
        
        if not enterprise:
            self.stdout.write(self.style.ERROR('Nenhuma empresa encontrada no banco de dados.'))
            return
        
        self.stdout.write(f'Empresa encontrada: {enterprise}')

        # List of Brazilian cities
        cities = [
            'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília',
            'Curitiba', 'Fortaleza', 'Manaus', 'Recife', 'Porto Alegre'
        ]

        # List of Brazilian states
        states = [
            'SP', 'RJ', 'MG', 'BA', 'DF', 'PR', 'CE', 'AM', 'PE', 'RS'
        ]

        # Create 20 fictional clients
        for i in range(20):
            try:
                name = fake.name()
                email = fake.email()
                phone = fake.phone_number()
                company = fake.company()
                city = random.choice(cities)
                state = random.choice(states)
                address = f"{fake.street_address()}, {city} - {state}"
                notes = fake.text(max_nb_chars=200)

                client = Client.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    company=company,
                    address=address,
                    notes=notes,
                    enterprise=enterprise,
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f'Cliente {i+1} criado: {name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao criar cliente {i+1}: {str(e)}'))

        total_clients = Client.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal de clientes no banco de dados: {total_clients}')) 