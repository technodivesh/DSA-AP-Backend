from django.utils.deprecation import MiddlewareMixin
from re import sub
from rest_framework.authtoken.models import Token

class ProcessRequestMiddleware(MiddlewareMixin):

  def process_view(self, request, view_func, view_args, view_kwargs):
    token_header = request.META.get('HTTP_AUTHORIZATION', None)
    if token_header:
      try:
        token = token_header.split(' ')[1]
        token_obj = Token.objects.get(key = token)
        request.user = token_obj.user
      except Token.DoesNotExist:
        pass
    print (request.user)



class UserTypeMiddleware(MiddlewareMixin):

  def process_view(self, request, view_func, view_args, view_kwargs):
    # if request.user.email:
    if str(request.user) != 'AnonymousUser':
      if (request.user.email == request.user.owner) or (not request.user.owner):
        request.user.is_manager = True
        request.user.is_employee = False
      else:
        request.user.is_manager = False
        request.user.is_employee = True
