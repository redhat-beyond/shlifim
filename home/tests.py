import pytest
from django.urls import reverse
from django.test import Client
from .models import Question


@pytest.mark.django_db
def test_explore_page_url():
    url = reverse('explore-page')
    c = Client()
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("question_id, expected_result", [
    ("1", 1),
    ("2", 1),
    ("3", 0),
    ("4", 0),
])
@pytest.mark.django_db
def test_answers_num_func(question_id, expected_result):
    question = Question.objects.get(id=question_id)
    answers_num = question.get_answers_num()
    assert answers_num == expected_result
