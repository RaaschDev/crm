from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from django.conf import settings
from apps.clients.models import Client
from apps.employers.models import Employer
from apps.tasks.models import Task
from apps.department.models import Department

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        # Template base para o prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente virtual especializado em ajudar com informações sobre a empresa.\nResponda de forma clara e concisa, usando apenas as informações disponíveis.\nSe não souber a resposta, diga que não tem essa informação."""),
            ("human", "{input}")
        ])
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            verbose=True
        )

    def get_company_data(self):
        """Obtém dados da empresa para o contexto do chat"""
        clients = Client.objects.all()
        employers = Employer.objects.all()
        tasks = Task.objects.all()
        departments = Department.objects.all()

        context = (
            "Clientes:\n" + "\n".join([f"- {c.name} ({c.email})" for c in clients]) + "\n\n" +
            "Funcionários:\n" + "\n".join([f"- {e.name} - {e.position}" for e in employers]) + "\n\n" +
            "Tarefas:\n" + "\n".join([f"- {t.title} - Status: {t.status}" for t in tasks]) + "\n\n" +
            "Departamentos:\n" + "\n".join([f"- {d.name} - {d.employer_set.count()} funcionários" for d in departments])
        )
        return context

    def register_employee(self, name, position, department_id):
        """Registra um novo funcionário"""
        try:
            department = Department.objects.get(id=department_id)
            employer = Employer.objects.create(
                name=name,
                position=position,
                department=department
            )
            return f"Funcionário {name} registrado com sucesso!"
        except Department.DoesNotExist:
            return "Departamento não encontrado."
        except Exception as e:
            return f"Erro ao registrar funcionário: {str(e)}"

    def update_employee(self, employee_id, name=None, position=None, department_id=None):
        """Atualiza dados de um funcionário existente"""
        try:
            employer = Employer.objects.get(id=employee_id)
            if name:
                employer.name = name
            if position:
                employer.position = position
            if department_id:
                department = Department.objects.get(id=department_id)
                employer.department = department
            employer.save()
            return f"Funcionário {employer.name} atualizado com sucesso!"
        except Employer.DoesNotExist:
            return "Funcionário não encontrado."
        except Department.DoesNotExist:
            return "Departamento não encontrado."
        except Exception as e:
            return f"Erro ao atualizar funcionário: {str(e)}"

    def get_response(self, message):
        """Obtém resposta do modelo para a mensagem do usuário"""
        context = self.get_company_data()
        full_input = f"{context}\n\nPergunta: {message}"
        response = self.chain.run(input=full_input)
        return response

    def analyze_employee(self, employee_id):
        """Analisa um funcionário específico e retorna informações detalhadas"""
        try:
            employer = Employer.objects.get(id=employee_id)
            return f"Funcionário: {employer.name}\nPosição: {employer.position}\nDepartamento: {employer.department.name}"
        except Employer.DoesNotExist:
            return "Funcionário não encontrado."

    def analyze_department(self, department_id):
        """Analisa um departamento específico e retorna informações detalhadas"""
        try:
            department = Department.objects.get(id=department_id)
            employees = department.employer_set.all()
            return f"Departamento: {department.name}\nFuncionários: {', '.join([e.name for e in employees])}"
        except Department.DoesNotExist:
            return "Departamento não encontrado."

    def analyze_task(self, task_id):
        """Analisa uma tarefa específica e retorna informações detalhadas"""
        try:
            task = Task.objects.get(id=task_id)
            return f"Tarefa: {task.title}\nStatus: {task.status}\nDescrição: {task.description}"
        except Task.DoesNotExist:
            return "Tarefa não encontrada."

    def get_all_clients(self):
        """Retorna todos os dados sobre os clientes"""
        clients = Client.objects.all()
        return "\n".join([f"Cliente: {c.name}\nEmail: {c.email}\nTelefone: {c.phone}\nEndereço: {c.address}" for c in clients]) 