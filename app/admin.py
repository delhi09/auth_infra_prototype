from .models import Company, Contract, Employee, Service
from django.contrib import admin

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Contract)
