import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.clients.models import Client
from apps.enterprise.models import Enterprise

fake = Faker('pt_BR')

def create_fictional_clients():
    print("Iniciando criação de clientes fictícios...")
    
    # Get the first enterprise from the database
    enterprise = Enterprise.objects.first()
    
    if not enterprise:
        print("Erro: Nenhuma empresa encontrada no banco de dados.")
        return
    
    print(f"Empresa encontrada: {enterprise}")

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
            print(f"Cliente {i+1} criado: {name}")
        except Exception as e:
            print(f"Erro ao criar cliente {i+1}: {str(e)}")

    print("\nVerificando clientes criados...")
    total_clients = Client.objects.count()
    print(f"Total de clientes no banco de dados: {total_clients}")

if __name__ == '__main__':
    create_fictional_clients() 