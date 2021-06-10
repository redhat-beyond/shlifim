from home.models import Answer
import pytest


@pytest.mark.django_db
class TestAddAnswer:
    @pytest.fixture
    def comment_content(self):
        return {"content": "test"}

    def test_post_redirect(
        self, client, question_test_data, authenticated_user, comment_content
    ):
        response = client.post(
            f"/explore/question_{question_test_data.id}/", data=comment_content
        )
        assert response.status_code == 302  # check that redirect
        # redirect back to the same display question page
        assert response.url == f"/explore/question_{question_test_data.id}/"

    def test_add_answer_post(
        self, authenticated_user, client, question_test_data, comment_content
    ):
        client.post(f"/explore/question_{question_test_data.id}/", data=comment_content)
        answers_feed = question_test_data.get_answers_feed()
        assert (
            answers_feed.first().id
        )  # check if there is answer to the question_test_data
        assert (
            answers_feed.first().content == "test"
        )  # answer content saved as expected.
        assert (
            answers_feed.first().profile.user == authenticated_user
        )  # answer profile is the user that posted.

    def test_html_authenticated_user_form_visible(
        self, authenticated_user, question_test_data, client
    ):
        response = client.get(f"/explore/question_{question_test_data.id}/")
        # comment-form is the div id of the comment-form, should be visible (because it is authenticated user)
        assert "comment-form" in str(response.content)
        # not-authenticated is the div for login button for not authenticated user, should be hidden
        assert "not-authenticated" not in str(response.content)

    def test_html_not_authenticated_user_form_visible(self, question_test_data, client):
        response = client.get(f"/explore/question_{question_test_data.id}/")
        # should be hidden for not authenticated user
        assert "comment-form" not in str(response.content)
        # login button for not authenticated user should be visible
        assert "not-authenticated" in str(response.content)

    def test_default_params_answer(self, profile, question_test_data):
        answer = Answer(profile=profile, question=question_test_data, content="test")
        assert answer.is_edited is False

    def test_get_answers(self):
        out = Answer.get_answers_by_date()
        assert all(isinstance(a, Answer) for a in out)
        assert set(
            [
                (2, 2, "IDK"),
                (
                    1,
                    1,
                    "pretty sure its 2 but I suggesting you to check with another resources ",
                ),
            ]
        ).issubset(list(out.values_list("profile", "question", "content")))

    def test_post_answer_not_authenticated_user(
        self, client, question_test_data, comment_content
    ):
        response = client.post(
            f"/explore/question_{question_test_data.id}/", data=comment_content
        )
        assert response.status_code == 401

    def test_valid_tags_not_removed_from_answer(
        self, client, question_test_data, authenticated_user
    ):
        data = {"content": "<p>test</p>"}
        client.post(f"/explore/question_{question_test_data.id}/", data=data)
        answer = question_test_data.get_answers_feed().first()
        assert "<p>" in answer.content

    def test_invalid_tags_removed_from_question(
        self, client, question_test_data, authenticated_user
    ):
        data = {
            "content": '<script language = "javascript" > alert("You are PWNED!") </script>'
        }
        client.post(f"/explore/question_{question_test_data.id}/", data=data)
        answer = question_test_data.get_answers_feed().first()
        assert "<script>" not in answer.content
