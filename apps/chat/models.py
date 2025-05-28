from django.db import models
from django.contrib.auth import get_user_model
from utils.models import BaseModel

User = get_user_model()

class Chat(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    message = models.TextField(verbose_name='Mensagem')
    response = models.TextField(verbose_name='Resposta')
    is_processed = models.BooleanField(default=True, verbose_name='Processado')

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat de {self.user.username} - {self.created_at}"
