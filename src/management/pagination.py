from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Country, EmployeeAuthPC
from django.db.models import Q


class PCPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'records'
    max_page_size = 1000


class ClientCountryPgNumPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'records'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'unique_count': Country.objects.all().values('country_code').distinct().count(),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })


class PCMappingRequestPgNumPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'records'
    max_page_size = 100


class ProfitCenterMappingListPgNumPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'records'
    max_page_size = 100

    def get_paginated_response(self, data):
        if self.request.user.is_admin:
            pc_queryset = EmployeeAuthPC.objects.filter(
                status=1).values('profit_center_code')
            ctry_queryset = EmployeeAuthPC.objects.filter(
                status=1).values('country_code')
        elif self.request.user.is_owner:
            pc_queryset = EmployeeAuthPC.objects.filter(
                employee_code__owner=self.request.user.employee_code, status=1).values('profit_center_code')
            ctry_queryset = EmployeeAuthPC.objects.filter(
                employee_code__owner=self.request.user.employee_code, status=1).values('country_code')
        else:
            pc_queryset = EmployeeAuthPC.objects.filter(
                employee_code=self.request.user.employee_code, status=1).values('profit_center_code')
            ctry_queryset = EmployeeAuthPC.objects.filter(
                employee_code=self.request.user.employee_code, status=1).values('country_code')
        return Response({
            'pc_count': pc_queryset.distinct().count(),
            'ctry_count': ctry_queryset.distinct().count(),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
