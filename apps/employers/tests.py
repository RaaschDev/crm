from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.department.models import Department
from apps.enterprise.models import Enterprise
from .models import Employer

User = get_user_model()

class EmployerModelTest(TestCase):
    def setUp(self):
        self.enterprise = Enterprise.objects.create(
            name='Empresa Teste',
            cnpj='12345678901234',
            email='empresa@teste.com',
            phone='1234567890'
        )
        
        self.department = Department.objects.create(
            name='Departamento Teste',
            description='Descrição do departamento teste',
            enterprise=self.enterprise
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            enterprise=self.enterprise
        )
        
        self.employer = Employer.objects.create(
            name='Funcionário Teste',
            email='funcionario@teste.com',
            phone='1234567890',
            position='Cargo Teste',
            department=self.department,
            enterprise=self.enterprise,
            user=self.user
        )

    def test_employer_creation(self):
        self.assertTrue(isinstance(self.employer, Employer))
        self.assertEqual(self.employer.__str__(), self.employer.name)
        self.assertEqual(self.employer.name, 'Funcionário Teste')
        self.assertEqual(self.employer.email, 'funcionario@teste.com')
        self.assertEqual(self.employer.phone, '1234567890')
        self.assertEqual(self.employer.position, 'Cargo Teste')
        self.assertEqual(self.employer.department, self.department)
        self.assertEqual(self.employer.enterprise, self.enterprise)
        self.assertEqual(self.employer.user, self.user)
        self.assertTrue(self.employer.is_active)
