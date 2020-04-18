from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
import pytest

from .factories import UserFactory
from ..serializers import CreateUserSerializer


@pytest.fixture
def user_data():
    return model_to_dict(UserFactory.build())

@pytest.mark.django_db
def test_serializer_with_empty_data(user_data):
    serializer = CreateUserSerializer(data={})
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_serializer_with_valid_data(user_data):
    serializer = CreateUserSerializer(data=user_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_serializer_hashes_password(user_data):
    serializer = CreateUserSerializer(data=user_data)
    assert serializer.is_valid()

    user = serializer.save()
    assert check_password(user_data.get('password'), user.password)
