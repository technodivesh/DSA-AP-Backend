from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .helper.graph import *
from .models import t_Employee
from .serializers import UserSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .pagination import UserPgNumPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser,IsAuthenticated


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class User(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        User details

        Returns logged-in user details 
        ## URL endpoint
        ```
        GET  /user/details/
        ```
        ## Response

        ```
        {
            "email": "user@example.com",
            "password": "string",
            "last_login": "2019-08-24T14:15:22Z",
            "employee_name": "string",
            "work_country": "string",
            "sbu": "string",
            "jot_title": "string",
            "create_date_time": "2019-08-24T14:15:22Z",
            "exit_date_time": "2019-08-24T14:15:22Z",
            "employee_code": "string",
            "is_active": true,
            "is_admin": true,
            "owner": "string"
        }
        ```
        """
        try:

            users_obj = t_Employee.objects.get(email=request.user.email)
            serialize = UserSerializer(users_obj)
            data = serialize.data
            
        except t_Employee.DoesNotExist:
            data = {
                'error': True,
                'error_string': "User not found"
            }
            logger.debug(f"{data}")
            return Response(data,status=status.HTTP_204_NO_CONTENT)
        return Response(data,status=status.HTTP_200_OK)


class OAuth(APIView):

    def post(self, request, format=None):
        """
        User Login

        If user exists on AAD (Azure Active Directory), userPrincipalName will be checked in  EmailID,EmailByCode and EmailByName to Authenticate

        ## URL endpoint
        ```
        GET  /user/login/
        ```
        ## Request
        ```
        {
            'accessToken':"string (AAD)"
        }
        ```

        ## Response

        ```
        {
            'token': "token-key-string",
            'email': "user@example.com",
            'code': "string"
            'name': "string"
            'is_owner': "bool"
        }
        ```
        """
        try:
            user_detail = get_user(request.data['accessToken'])
            user = t_Employee.objects.get(
                Q(email=user_detail['userPrincipalName']) | 
                Q(email_by_code=user_detail['userPrincipalName']) |
                Q(email_by_name=user_detail['userPrincipalName'])
            )
            
            token_obj = Token.objects.get_or_create(user=user)
            data = {
                'token': token_obj[0].key,
                'email': user.email,
                'code': user.employee_code,
                'name': user.employee_name,
                'is_owner': user.is_owner
            }

        except t_Employee.DoesNotExist:
            data = {
                'error': True,
                'error_string': "User does not exists"
            }
            logger.debug(f"{data}, logged in failed")
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)

        except KeyError:
            data = {
                'error': True,
                'error_string': "Forbibben"
            }
            logger.debug(f"{data}, logged in failed")
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        
        logger.info(f"{user.employee_code}:{user.employee_name} logged in")
        return Response(data)

class UserListView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    """
    Employee List

    Returns a list of all users active for this Portal.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/sample

    ## URL endpoint
        ```
        GET  /user/list/
        ```
    ## Response

    ```
    {
    "count": 0,
    "next": "http://example.com",
    "previous": "http://example.com",
    "results": [
        {
            "employee_code": "string",
            "last_login": "2019-08-24T14:15:22Z",
            "employee_name": "string",
            "email": "user@example.com",
            "email_by_code": "user@example.com",
            "email_by_name": "user@example.com",
            "work_country": "string",
            "sbu": "string",
            "owner_name": "string",
            "owner_email": "user@example.com",
            "job_title": "string",
            "create_date_time": "2019-08-24T14:15:22Z",
            "exit_date_time": "2019-08-24T14:15:22Z",
            "is_active": true,
            "is_admin": true,
            "is_owner": true,
            "password": "string",
            "owner": "string"
        }
    ]
    }
    ```
    """
    queryset = t_Employee.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPgNumPagination
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    search_fields = [
        "employee_name",
        "email"
    ]
    ordering_fields = [
        'employee_name'
    ]
    filterset_fields = (
        'employee_name',
        'employee_code',
    )

    def get_queryset(self):

        try:

            if self.request.user.is_admin:
                queryset = t_Employee.objects.all()
            elif self.request.user.is_owner:
                queryset = t_Employee.objects.filter(owner=self.request.user.employee_code)
            else:
                queryset = t_Employee.objects.filter(employee_code=self.request.user.employee_code)
            return queryset
        except Exception as err:
            logger.debug(str(err))

class UserView(APIView):

    permission_classes = (IsAdminUser,)
    """
    Update user details 
    """
    def post(self, request, format=None):
        """
        Update User details

        ## URL endpoint
        ```
        POST  /user/update/
        ```
        ## Request

        ```
        {
            "employee_name": "string",
            "work_country": "string",
            "sbu": "string",
            "employee_code": "string",
            "owner": "string"
        }
        ```

        ## Response

        ```
        {
            'token': "token-key-string",
            'email': "user@example.com",
            'code': "string"
        }
        ```
        """
        try:
            user_obj = t_Employee.objects.get(email=request.user.email)
            if 'sbu' in request.data:
                user_obj.sbu = request.data['sbu']
            if 'employee_code' in request.data:
                user_obj.employee_code = request.data['employee_code']
            # if 'owner' in request.data:
            if request.data['owner']:
                user_obj.owner = t_Employee.objects.filter(email__icontains=request.data['owner']).first()
            if 'work_country' in request.data:
                user_obj.work_country = request.data['work_country']
            user_obj.save()
            user = user_obj
            token_obj = Token.objects.get_or_create(user=user_obj)
            data = {
                'token': token_obj[0].key,
                'sbu': user.sbu,
                'employee_code': user.employee_code,
                'success': True, 
            }
            logger.info(data)
        except Exception as exc:
            data = {
                'error': str(exc), 
                'success': False, 
                'error': True,
                'message': 'Failed To Update.'
            }
            logger.debug(data)
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            
        return Response(data, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        User logout

        ## URL endpoint
        ```
        POST  /user/logout/
        ```
        """
        try:
            token = request.headers.get('Authorization')
            token = token.split(' ')[1]
            token_obj = Token.objects.get(key = token)
            token_obj.delete()
            logger.info(f"{request.user.employee_code}:{request.user.employee_name} logged out")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.debug("Error",e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
