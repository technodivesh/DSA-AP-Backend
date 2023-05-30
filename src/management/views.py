from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from login.models import t_Employee
from .models import EmployeeRequestHistory, EmployeeAuthPC, ProfitCenter, Country
from .serializers import *
from django.forms.models import model_to_dict
from datetime import datetime
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from .pagination import *
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Count
import sys
import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveUpdateAPIView
from .filters import *


import logging
logger = logging.getLogger(__name__)

# Create your views here.


class CountryListView(ListAPIView):
    """
    GET Country List

    ## URL endpoint
    ```
    GET  /emp/country/
    ```
    ## Response

    ```
    {
        "count": 0,
        "next": "http://example.com",
        "previous": "http://example.com",
        "results": [
            {
            "id": 0,
            "client": -2147483648,
            "country_code": "st",
            "country_name": "string",
            "region": "string",
            "geography": "string",
            "region_value": "string",
            "created_date": "2019-08-24T14:15:22Z",
            "updated_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
    ```
    """

    # queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = ClientCountryPgNumPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "country_code",
        "country_name",
        "region",
        "geography",
    ]
    ordering_fields = [
        'country_name'
    ]
    filterset_fields = (
        'country_code',
        'country_name',
    )

    def get_queryset(self):
        '''
        Optionally restricts the returned Countries,
        by filtering against a `client` query parameter in the URL.
        '''
        queryset = Country.objects.all()
        client = self.request.query_params.get('client', None)
        if client:
            queryset = queryset.filter(client=client)
        return queryset


class EmpRequestHistoryView(ListAPIView):

    """
    PC mapping request list

    Returns a list of PC mapping requests raised by users for approval.


    ## URL endpoint
    ```
    GET  /emp/pc_mapping_req_history
    ```
    ## Response

    ```
    {
        "count": 0,
        "next": "http://example.com",
        "previous": "http://example.com",
        "results": [
            {
            "id": 0,
            "country_code": "string",
            "pc_code": "string",
            "pc_desc": "string",
            "requester_name": "string",
            "status": "string",
            "comments": "string",
            "created_date": "2019-08-24T14:15:22Z",
            "updated_date": "2019-08-24T14:15:22Z",
            "start_date": "2019-08-24T14:15:22Z",
            "end_date": "2019-08-24T14:15:22Z",
            "requester_id": "string",
            "profit_center_code": 0,
            "approver_id": "string",
            "country_id": 0,
            "created_by": "string",
            "updated_by": "string"
            }
        ]
    }
    ```
    """
    # queryset = EmployeeRequestHistory.objects.all()
    serializer_class = EmployeeRequestHistorySerializer
    pagination_class = PCMappingRequestPgNumPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = EmployeeRequestHistoryFilter
    permission_classes = [IsAuthenticated]
    search_fields = [
        "requester_id__email",
        "requester_id__employee_name",
        "approver_id__email",
        "approver_id__employee_name",
        "profit_center_id__profit_center_desc",
        "country_id__country_name",
        "country_id__region",
    ]
    ordering_fields = [
        '-id'
    ]

    def get_queryset(self):

        if self.request.user.is_admin:
            queryset = EmployeeRequestHistory.objects.all()
        elif self.request.user.is_owner:
            queryset = EmployeeRequestHistory.objects.filter(
                approver_id=self.request.user.employee_code)
        else:
            queryset = EmployeeRequestHistory.objects.filter(
                requester_id=self.request.user.employee_code)
        return queryset


class Post_pc_mapping_req(CreateAPIView):
    """
    POST: PC mapping request
    """
    serializer_class = EmployeeRequestHistorySerializer
    queryset = EmployeeRequestHistory.objects.all()

    # def get_serializer(self, instance=None, data=None, many=False, partial=False):
    #     return super(Post_pc_mapping_req, self).get_serializer(instance=instance, data=data, many=True, partial=partial)

    def post(self, request, *args, **kwargs):

        draft_request_data = self.request.data.copy()
        data = {}
        try:
            for pc_id in self.request.data["profit_center_code"]:
                draft_request_data["profit_center"] = pc_id

                if request.data.get('requester_id'):
                    # _requester_code = t_Employee.objects.get(email=request.data.get('requester_id')).employee_code
                    _requester_code = request.data.get('requester_id')
                else:
                    _requester_code = request.user.employee_code

                draft_request_data["requester"] = _requester_code
                approver = t_Employee.objects.get(
                    employee_code=draft_request_data["requester"]).owner
                if approver:
                    draft_request_data["approver"] = approver.employee_code
                draft_request_data["created_by"] = request.user.employee_code
                draft_request_data["updated_by"] = request.user.employee_code
                draft_request_data["country"] = draft_request_data["country_id"]
                logger.info(f"{draft_request_data}")
                serializer = EmployeeRequestHistorySerializer(
                    data=draft_request_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data = serializer.data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.debug(f"{exc_type}")
        return Response(data)


class DashboardInfo(APIView):

    def get(self, request):
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
        })


class PCMappingDelete(RetrieveUpdateAPIView):

    queryset = EmployeeAuthPC.objects.all()
    serializer_class = EmployeeAuthPCSerializer

    def update(self, request, *args, **kwargs):
        # request.data['updated_by'] = request.user.email
        logger.info(request.data)
        request.data['end_date'] = datetime.now()
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Updated Successfully", "data": serializer.data})


class ProfitCenterMappingListView(ListAPIView):

    """
    GET List of mapped PC with a Employee

    Returns a list of mapped PC.


    ## URL endpoint
    ```
    GET  /emp/emp_pc_mapping
    ```
    ## Response

    ```
    {
    "count":0,
    "next":"http://example.com",
    "previous":"http://example.com",
    "results":[
        {
            "id":0,
            "pc_desc":"string",
            "pc_code":"string",
            "requester":"string",
            "approver":"string",
            "country_code":"st",
            "profit_center_code":"string",
            "start_date":"2019-08-24T14:15:22Z",
            "end_date":"2019-08-24T14:15:22Z",
            "status":true,
            "country":0,
            "employee_code":"string",
            "profit_center":0,
            "customer_group_id":0
        }
    ]
    }
    ```
    """
    # queryset = EmployeeAuthPC.objects.all()
    serializer_class = EmployeeAuthPCSerializer
    pagination_class = ProfitCenterMappingListPgNumPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "employee_code__email",
        "employee_code__employee_code",
        "employee_code__employee_name",
        "profit_center__profit_center_code",
        "profit_center__profit_center_desc",
        "country_code",
        "country__country_name",
        "country__region",
    ]
    ordering_fields = [
        '-id'
    ]
    filter_class = EmployeeAuthPCFilter

    def get_queryset(self):
        """
        This view should return a list of all the mapped emp-pc
        for the currently authenticated user.
        For Admin: All records
        For Owner: Records of subordinates
        For Employee: Records of loged-in user only
        """

        if self.request.user.is_admin:
            queryset = EmployeeAuthPC.objects.all()
        elif self.request.user.is_owner:
            queryset = EmployeeAuthPC.objects.filter(
                employee_code__owner=self.request.user.employee_code)
        else:
            queryset = EmployeeAuthPC.objects.filter(
                employee_code=self.request.user.employee_code)
        return queryset


class EmployeePCRequestApproval(UpdateAPIView):
    "Update (Approve/Reject) PC mapping request"
    queryset = EmployeeRequestHistory.objects.all()
    serializer_class = EmployeeRequestHistorySerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.employee_code
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Insert data into eployee auth pc
            data = {}
            if request.data['status'] == "Approved":
                employee_auth_pc_obj, created = EmployeeAuthPC.objects.update_or_create(
                    country=instance.country,
                    employee_code=instance.requester,
                    profit_center=instance.profit_center,
                    defaults={
                        'status': True,
                        'country': instance.country,
                        'employee_code': instance.requester,
                        # 'customer_group_id' : None
                        'profit_center': instance.profit_center,
                        'start_date': instance.start_date,
                        'end_date': instance.end_date,
                    }
                )
                data = model_to_dict(employee_auth_pc_obj)

            return Response({"message": "Updated Successfully", "data": data})

        else:
            return Response({"message": "failed", "details": serializer.errors})


class ProfitCenterListView(ListAPIView):

    """
    List of all Profit Centers 

    ## URL endpoint
    ```
    GET  /emp/pc
    ```
    ## Response

    ```
    {
        "count": 0,
        "next": "http://example.com",
        "previous": "http://example.com",
        "results": [
            {
            "id": 0,
            "client": -2147483648,
            "profit_center_code": "string",
            "profit_center_desc": "string",
            "company_code": "stri",
            "business_line": "string",
            "business_geography": "string",
            "business_segment": "string",
            "mis_business_vertical": "string",
            "mis_business_unit": "string",
            "business_brand": "string",
            "product_group": "string",
            "flash_pg": "string",
            "me_tel_pg": "string",
            "is_active": true,
            "created_date": "2019-08-24T14:15:22Z",
            "updated_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
    ```
    """
    queryset = ProfitCenter.objects.all()
    serializer_class = ProfitCenterSerializer
    pagination_class = PCPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "profit_center_code",
        "profit_center_desc",
        "company_code",
        "business_line",
        "business_geography",
        "business_segment",
    ]
    ordering_fields = [
        '-updated_date'
    ]

    filter_class = ProfitCenterFilter
    # filterset_fields = (
    #     'profit_center_code',
    #     'profit_center_desc',
    #     'business_brand',
    # )


class ProfitCenterDetail(RetrieveUpdateDestroyAPIView):
    """
    GET detail of one record, PUT, PATCH, DELETE that record.

    ## URL endpoint
    ```
    GET  /emp/pc/{id}
    ```
    ## Response

    ```
    {
        "count": 0,
        "next": "http://example.com",
        "previous": "http://example.com",
        "results": [
            {
            "id": 0,
            "client": -2147483648,
            "profit_center_code": "string",
            "profit_center_desc": "string",
            "company_code": "stri",
            "business_line": "string",
            "business_geography": "string",
            "business_segment": "string",
            "mis_business_vertical": "string",
            "mis_business_unit": "string",
            "business_brand": "string",
            "product_group": "string",
            "flash_pg": "string",
            "me_tel_pg": "string",
            "is_active": true,
            "created_date": "2019-08-24T14:15:22Z",
            "updated_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
    ```
    """
    queryset = ProfitCenter.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProfitCenterDetailSerializer
