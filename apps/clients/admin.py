from django.contrib import admin
from .models import Client, ClientTag

# Register your models here.

admin.site.register(Client)
admin.site.register(ClientTag)