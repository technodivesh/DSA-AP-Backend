import pytest
# from django.contrib.auth.models import User
from login.models import t_Employee

@pytest.mark.django_db
def test_create_user():
    t_Employee.objects.create_user('test','test@test.com')
    assert t_Employee.objects.count() == 1

@pytest.fixture()
def user_1(db):
    user = t_Employee.objects.create_user("test-user@test.com")
    print("create test-user")
    return user

def test_create_user_1(user_1):
    print("check user")
    assert user_1.email == "test-user@test.com"
