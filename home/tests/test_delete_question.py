import pytest
from django.urls import reverse
from home.models import Question

TEST_QUESTION_ID = 1
TEST_SECOND_QUESTION_ID = 3


@pytest.mark.django_db
def test_delete_button_visible(logged_client):
    response = logged_client.get(reverse("question-detail", args=[TEST_QUESTION_ID]))
    char_content = response.content.decode(response.charset)
    assert 'value="Delete"' in char_content


@pytest.mark.django_db
def test_delete_button_invisible(client):
    response = client.get(reverse("question-detail", args=[TEST_QUESTION_ID]))
    char_content = response.content.decode(response.charset)
    assert 'value="Delete"' not in char_content


@pytest.mark.django_db
def test_unsigned_user_delete(client):
    response = client.post(reverse("question-delete", args=[TEST_SECOND_QUESTION_ID]))
    assert response.status_code == 401


@pytest.mark.django_db
def test_unauthorized_user_delete(logged_client):
    response = logged_client.post(
        reverse("question-delete", args=[TEST_SECOND_QUESTION_ID])
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_legit_delete_post(logged_client):
    response = logged_client.post(reverse("question-delete", args=[TEST_QUESTION_ID]))
    assert response.status_code == 302
    assert response.url == reverse("explore-page")
    assert not Question.objects.all().filter(id=TEST_QUESTION_ID).exists()


@pytest.mark.django_db
def test_delete_question_success_msg(logged_client):
    response = logged_client.post(reverse("question-delete", args=[TEST_QUESTION_ID]))
    response = logged_client.get(response.url)
    messages = list(response.context["messages"])
    assert len(messages) == 1
    assert str(messages[0].message) == "SUCCESS: Your question has been deleted."
