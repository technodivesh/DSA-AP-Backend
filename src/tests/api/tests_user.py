from urllib import response
import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = dict(
        # first_name="Divesh",
        # last_name="Chandolia",
        email="*********",
        password="*********",
        accessToken="********"
    )

    response = client.post('/user/login',payload)
    assert response.status_code == 200

