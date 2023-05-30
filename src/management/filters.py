
from django_filters import rest_framework as filters
from .models import  (
    EmployeeAuthPC, 
    EmployeeRequestHistory,
    ProfitCenter
)

from django_filters.constants import EMPTY_VALUES

class ListFilter(filters.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs

class EmployeeAuthPCFilter(filters.FilterSet):
    
    pc_code = filters.CharFilter(field_name="profit_center_code",lookup_expr='contains')
    pc_desc = filters.CharFilter(field_name="profit_center__profit_center_desc",lookup_expr='icontains')
    requester = filters.CharFilter(field_name="employee_code__employee_name",lookup_expr='icontains')
    approver = filters.CharFilter(field_name="employee_code__owner__employee_name",lookup_expr='icontains')
    country_code = filters.CharFilter(field_name="country__country_name",lookup_expr='icontains')

    class Meta:
        model = EmployeeAuthPC
        fields = [
            'country_code', 
            'pc_code', 
            'pc_desc', 
            'requester', 
            'approver', 
            'status', 
        ]


class EmployeeRequestHistoryFilter(filters.FilterSet):
    
    pc_code = filters.CharFilter(field_name="profit_center_id__profit_center_code",lookup_expr='contains')
    pc_desc = filters.CharFilter(field_name="profit_center_id__profit_center_desc",lookup_expr='icontains')
    requester_name = filters.CharFilter(field_name="requester_id__employee_name",lookup_expr='icontains')
    approver_name = filters.CharFilter(field_name="approver_id__employee_name",lookup_expr='icontains')
    country_code = filters.CharFilter(field_name="country_id__country_name",lookup_expr='icontains')
    status = ListFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = EmployeeRequestHistory
        fields = [
            'country_code', 
            'pc_code', 
            'pc_desc', 
            'requester_name', 
            'approver_name', 
            'status'
        ]

class ProfitCenterFilter(filters.FilterSet):
    
    profit_center_code = filters.CharFilter(field_name="profit_center_code",lookup_expr='contains')
    profit_center_desc = filters.CharFilter(field_name="profit_center_desc",lookup_expr='icontains')
    company_code = filters.CharFilter(field_name="company_code",lookup_expr='icontains')
    business_line = filters.CharFilter(field_name="business_line",lookup_expr='icontains')
    business_geography = filters.CharFilter(field_name="business_geography",lookup_expr='icontains')
    business_segment = filters.CharFilter(field_name="business_segment",lookup_expr='icontains')
    mis_business_vertical = filters.CharFilter(field_name="mis_business_vertical",lookup_expr='icontains')
    mis_business_unit = filters.CharFilter(field_name="mis_business_unit",lookup_expr='icontains')
    business_brand = filters.CharFilter(field_name="business_brand",lookup_expr='icontains')
    product_group = filters.CharFilter(field_name="product_group",lookup_expr='icontains')
    flash_pg = filters.CharFilter(field_name="flash_pg",lookup_expr='icontains')
    me_tel_pg = filters.CharFilter(field_name="me_tel_pg",lookup_expr='icontains')
    business_unit = filters.CharFilter(field_name="business_unit",lookup_expr='icontains')
    sbu = filters.CharFilter(field_name="sbu",lookup_expr='icontains')

    class Meta:
        model = ProfitCenter
        fields = [
            "profit_center_code",
            "profit_center_desc",
            "company_code",
            "business_line",
            "business_geography",
            "business_segment",
            "mis_business_vertical",
            "mis_business_unit",
            "business_brand",
            "product_group",
            "flash_pg",
            "me_tel_pg",
            "business_unit",
            "sbu",
            "is_active",
        ]
