import pytest
from home.models import Profile, Subject, Question
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate


@pytest.fixture
def question_test_data():
    user = User.objects.get(username='Rebecca')
    profile = Profile.objects.get(user=user)
    subject = Subject.objects.get(subject_name='Physics')
    question = Question(profile=profile,
                        title='Question test data',
                        content='Will this question test data pass?',
                        publish_date=timezone.now(),
                        subject=subject,
                        sub_subject=None,
                        grade='10',
                        book=None,
                        book_page=None,
                        is_edited=False)
    question.save()
    return question


@pytest.fixture
def profile():
    profile = Profile.create(username="test_user", password="testtest", email="test@test.com")
    return profile


@pytest.fixture
def authenticated_user(client, request):
    username = 'Lior'
    password = 'LiorLior'
    client.login(username=username, password=password)
    user = authenticate(request, username=username, password=password)
    return user
