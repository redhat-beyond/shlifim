import pytest
from django.urls import reverse
from home.models import Question

TEST_QUESTION_ID = 1
TEST_SECOND_QUESTION_ID = 3


@pytest.mark.django_db
class TestDeleteQuestionFeature:
    question_detail_url_1 = reverse("question-detail", args=[TEST_QUESTION_ID])
    question_delete_url_1 = reverse("question-delete", args=[TEST_QUESTION_ID])
    question_delete_url_2 = reverse("question-delete", args=[TEST_SECOND_QUESTION_ID])

    def test_delete_button_visible(self, logged_client):
        response = logged_client.get(self.question_detail_url_1)
        char_content = response.content.decode(response.charset)
        assert 'value="Delete"' in char_content

    def test_delete_button_invisible(self, client):
        response = client.get(self.question_detail_url_1)
        char_content = response.content.decode(response.charset)
        assert 'value="Delete"' not in char_content

    def test_unsigned_user_delete(self, client):
        response = client.post(self.question_delete_url_2)
        assert response.status_code == 401

    def test_unauthorized_user_delete(self, logged_client):
        response = logged_client.post(self.question_delete_url_2)
        assert response.status_code == 401

    def test_legit_delete_post(self, logged_client):
        response = logged_client.post(self.question_delete_url_1)
        assert response.status_code == 302
        assert response.url == reverse("explore-page")
        assert not Question.objects.all().filter(id=TEST_QUESTION_ID).exists()

    def test_delete_question_success_msg(self, logged_client):
        response = logged_client.post(self.question_delete_url_1)
        response = logged_client.get(response.url)
        messages = list(response.context["messages"])
        assert len(messages) == 1
        assert str(messages[0].message) == "SUCCESS: Your question has been deleted."
