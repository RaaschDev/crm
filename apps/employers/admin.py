from django.contrib import admin
from .models import Employer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'position', 'department', 'enterprise', 'is_active')
    list_filter = ('is_active', 'department', 'enterprise')
    search_fields = ('name', 'email', 'phone', 'position')
    ordering = ('name',)
