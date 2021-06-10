import pytest
import pytz
from home.models import Profile, Subject, Question, Answer
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


LIKES_FEATURE_TEST_USER_ID = 1


@pytest.fixture
def question_test_data():
    user = User.objects.get(username="Rebecca")
    profile = Profile.objects.get(user=user)
    subject = Subject.objects.get(subject_name="Physics")
    question = Question(
        profile=profile,
        title="Question test data",
        content="Will this question test data pass?",
        publish_date=timezone.now(),
        subject=subject,
        sub_subject=None,
        grade="10",
        book=None,
        book_page=None,
        is_edited=False,
    )
    question.save()
    return question


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


@pytest.fixture
def logged_client(client):
    user = Profile.objects.all().get(user_id=LIKES_FEATURE_TEST_USER_ID).user
    client.force_login(user)
    return client


@pytest.fixture
def answers():
    profile = Profile.objects.first()
    question = Question.objects.get(id=3)
    ans1 = Answer(
        profile=profile,
        question=question,
        content="Answer 1",
        publish_date=datetime(2021, 4, 1, tzinfo=pytz.UTC),
        is_edited=False,
    )
    ans2 = Answer(
        profile=profile,
        question=question,
        content="Answer 2",
        publish_date=datetime(2021, 4, 2, tzinfo=pytz.UTC),
        is_edited=False,
    )
    ans1.save()
    ans2.save()
    return [ans1, ans2]
