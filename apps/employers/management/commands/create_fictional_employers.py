from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.employers.models import Employer
from apps.enterprise.models import Enterprise
from apps.department.models import Department
from faker import Faker
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria 30 funcionários fictícios no sistema'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        
        # Get the first enterprise from the database
        enterprise = Enterprise.objects.first()
        
        if not enterprise:
            self.stdout.write(self.style.ERROR('Nenhuma empresa encontrada no banco de dados.'))
            return
        
        self.stdout.write(f'Empresa encontrada: {enterprise}')

        # Get all departments
        departments = Department.objects.all()
        if not departments:
            self.stdout.write(self.style.ERROR('Nenhum departamento encontrado no banco de dados.'))
            return

        # List of common job positions
        positions = [
            'Analista de Sistemas',
            'Desenvolvedor Full Stack',
            'Desenvolvedor Frontend',
            'Desenvolvedor Backend',
            'Analista de Dados',
            'Analista de Suporte',
            'Analista de Infraestrutura',
            'Analista de Segurança',
            'Analista de Qualidade',
            'Analista de Negócios',
            'Analista de Projetos',
            'Analista de Marketing',
            'Analista de Vendas',
            'Analista de RH',
            'Analista Financeiro'
        ]

        # Create 30 fictional employers
        for i in range(30):
            try:
                # Create user first
                username = fake.user_name()
                email = fake.email()
                password = 'senha123'  # Senha padrão que pode ser alterada depois
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )

                # Create employer
                name = f"{user.first_name} {user.last_name}"
                phone = fake.phone_number()
                position = random.choice(positions)
                department = random.choice(departments)

                employer = Employer.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    position=position,
                    department=department,
                    enterprise=enterprise,
                    user=user,
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f'Funcionário {i+1} criado: {name} - {position}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao criar funcionário {i+1}: {str(e)}'))

        total_employers = Employer.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal de funcionários no banco de dados: {total_employers}')) 