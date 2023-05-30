from django.contrib import admin
from management.models import *


# Register your models here.
admin.site.register(CustomerGroup)
admin.site.register(EmployeeAuthDC)
admin.site.register(EmployeeAuthPC)
admin.site.register(EmployeeAuthSC)

@admin.register(ProfitCenter)
class ProfitCenterAdmin(admin.ModelAdmin):
    list_display = ['profit_center_code','company_code','client']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "country_code",
        "country_name",
        "region",
        "geography"
    ]

@admin.register(EmployeeRequestHistory)
class EmployeeRequestHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "profit_center",
        "requester",
        "approver",
        "country",
        "start_date",
        "end_date"
    ]

@admin.register(ProfitCenterStaging)
class ProfitCenterStagingAdmin(admin.ModelAdmin):
    list_display = [
        "profit_center_code",
        "profit_center_desc",
        "approver",
        "requester",
        "state",
    ]