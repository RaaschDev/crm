from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.enterprise.models import Enterprise
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True, blank=True)
    cpf = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        verbose_name='CPF',
        help_text='Digite o CPF no formato XXX.XXX.XXX-XX'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Telefone',
        help_text='Digite o telefone no formato (XX) XXXXX-XXXX'
    )
    photo = models.ImageField(upload_to='users/photos/', null=True, blank=True, verbose_name='Foto')
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']
    
    def __str__(self):
        return self.username