from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework import status
from faker import Faker
import factory
import pytest
from ..models import User
from .factories import UserFactory

fake = Faker()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user_data():
    return factory.build(dict, FACTORY_CLASS=UserFactory)


@pytest.fixture
def user_list_url():
    return reverse('user-list')


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user_detail_url(user):
    return reverse('user-detail', kwargs={'pk': user.pk})


@pytest.fixture
def client_with_cred(api_client):
    def make_credentialed_client(user=None):
        if user is None:
            user = UserFactory()
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        return api_client, user
    return make_credentialed_client


@pytest.mark.django_db
def test_post_request_with_no_data_fails(user_data, user_list_url, api_client):
    response = api_client.post(user_list_url, {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_request_with_valid_data_succeeds(user_data, user_list_url, api_client):
    response = api_client.post(user_list_url, user_data)
    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(pk=response.data.get('id'))
    assert user.username == user_data.get('username')
    assert check_password(user_data.get('password'), user.password)


@pytest.mark.django_db
def test_get_request_returns_a_given_user(user, user_detail_url, client_with_cred):
    client, _ = client_with_cred(user)
    response = client.get(user_detail_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_put_request_updates_a_user(user, user_detail_url, client_with_cred):
    client, _ = client_with_cred(user)

    new_first_name = fake.first_name()
    payload = {'first_name': new_first_name}
    response = client.put(user_detail_url, payload)
    assert response.status_code == status.HTTP_200_OK

    user = User.objects.get(pk=user.id)
    assert user.first_name == new_first_name
