import pytest
from django.contrib.auth.models import User
from users.models import Profile


@pytest.fixture
def profile():
    profile = Profile.create(
        username="test_user", password="testtest", email="test@test.com"
    )
    return profile


@pytest.fixture
def authenticated_user(client, request):
    user = User.objects.get(username="Lior")
    client.force_login(user)
    return user


@pytest.fixture
def valid_user_details():
    return {"username": "Lior", "password": "LiorLior"}
