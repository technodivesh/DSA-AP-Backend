from django.contrib import admin
from login.models import t_Employee

# Register your models here.

# admin.site.register(t_Employee)
@admin.register(t_Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "employee_name",
        "employee_code",
        "email",
        "email_by_code",
        "email_by_name",
        "work_country",
    ]