from django.urls import path, re_path

from .views import *

urlpatterns = [

    path('emp_pc_mapping/', ProfitCenterMappingListView.as_view(), name='ProfitCenterMappingList'),
    path('pc_mapping_req_history/', EmpRequestHistoryView.as_view(), name='PCMappingRequestHistory'),
    path('country/', CountryListView.as_view(), name='Country'),
    path('pc/', ProfitCenterListView.as_view(), name='ProfitCenter'),
    path('post_pc_mapping_req/', Post_pc_mapping_req.as_view(), name='Post_pc_mapping_req'), 
    path('pc_mapping_req_approval/<int:pk>', EmployeePCRequestApproval.as_view(), name='ApproveEmployeeRequest'),
    path('pc/<int:pk>',ProfitCenterDetail.as_view(),name='pc-detail'),
    path('emp_pc_mapping_delete/<int:pk>', PCMappingDelete.as_view(), name='ProfitCenterMappingDelete'),
    path('get_dashboad_info/', DashboardInfo.as_view(), name='DashboardInfo'),
]