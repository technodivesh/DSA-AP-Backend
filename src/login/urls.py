from django.urls import path

from .views import OAuth, UserView, UserListView, User, LogoutView

urlpatterns = [
    path('login/', OAuth.as_view(), name='OAuth2.0'),
    path('detail/', User.as_view(), name='UserDetail'),
    path('update/', UserView.as_view(), name='OAuth2.0'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    
]

