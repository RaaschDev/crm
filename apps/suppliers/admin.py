from django.contrib import admin
from .models import Supplier, SupplierTag

# Register your models here.
admin.site.register(Supplier)
admin.site.register(SupplierTag)
