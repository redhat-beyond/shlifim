import pytest
from home.models import Question
from django.urls import reverse
from django.db.models.query import QuerySet


DISLIKED_ANSWER_ID = 9
LIKED_ANSWER_ID = 10
INVALID_ANSWER_ID = 999999
TEST_QUESTION_ID = 14


@pytest.mark.django_db
class TestDisplayQuestionFeature:
    class TestAnswersManipulations:
        def test_set_is_edited(self, answers):
            """
            Tests functionality of set_is_edited
            """
            prev_is_edited_val = answers[0].is_edited
            answers[0].set_is_edited(not prev_is_edited_val)
            assert prev_is_edited_val != answers[0].is_edited

        @pytest.mark.django_db
        @pytest.mark.parametrize(
            ("filter_type, expected"), [("date", "Answer 2"), ("votes", "Answer 1")]
        )
        def test_answers_feed(self, filter_type, expected, answers):
            """
            Tests if get_answers_feed returns queryset of all the answers of
            question number 3 sorted by votes or answers
            """
            question = Question.objects.get(id=3)
            answers_feed = question.get_answers_feed(filter_type)
            assert isinstance(answers_feed, QuerySet)
            assert answers_feed[0].content == expected

    class TestQuestionRelatedMethods:
        def test_get_question_title(self):
            """
            get_question_title(question_id) returns a string for question
            should return question subject and question title
            """
            question = Question.objects.get(id=1)
            assert question.get_question_title() == "Math-question from math course"

    class TestHTMLRelated:
        @pytest.fixture
        def response(self, client):
            url = reverse("question-detail", args=[14])
            response = client.get(url)
            return response

        def test_display_question_page_url(self, response):
            """
            This test checks the returned status for routing to display-question feature
            """
            assert response.status_code == 200

        def test_template_name(self, response):
            assert response.templates[0].name == "home/question_detail.html"

        def test_response_context(self, response):
            """
            Testing if the context passed to the view contains the right contents
            """
            expected_pairs = [
                (
                    "question",
                    "Question #14 : g forwards, it was even later than ( 28/04/2021 23:14 )",
                ),
                (
                    "answers_tuples",
                    "[(<Answer: Answer B>, False, False), "
                    + "(<Answer: Answer A>, False, False), "
                    + "(<Answer: Popular Answer>, False, False), "
                    + "(<Answer: Old Answer>, False, False)]",
                ),
                ("answersCount", "4"),
                (
                    "tags",
                    "<QuerySet [{'id': 3, 'tag_name': 'Bagrut_Exam'}, "
                    + "{'id': 4, 'tag_name': 'Hebrew'}, {'id': 8, 'tag_name': 'java'}, "
                    + "{'id': 13, 'tag_name': 'all_my_sons'}]>",
                ),
                ("title", "History-g forwards, it was even later than"),
            ]
            for check, expected in expected_pairs:
                assert str(response.context[check]) == expected

        @pytest.mark.parametrize(
            ("filter_type, expected"),
            [("date", "Answer B"), ("votes", "Popular Answer")],
        )
        def test_sorting_answers(self, client, filter_type, expected):
            url = reverse("question-detail", args=[14])
            query_params = f"?sortanswersby={filter_type}"
            response = client.get(url + query_params)
            answer = response.context["answers_tuples"][0][0]
            assert str(answer.content) == expected

        def test_invalid_question_url(self, client):
            url = reverse("question-detail", args=[Question.objects.count() + 1])
            response = client.get(url)
            assert response.status_code == 404

        def test_invalid_answersort_url(self, client):
            url = reverse("question-detail", args=[1])
            query_params = "?sortanswersby=BAD"
            response = client.get(url + query_params)
            assert response.status_code == 404

    class TestThumbsRouting:
        def test_logged_user_good_route(self, logged_client):
            response = logged_client.get(
                f"/explore/question_{TEST_QUESTION_ID}/thumb/up/{DISLIKED_ANSWER_ID}"
            )
            assert response.status_code == 302
            assert response.url == f"/explore/question_{TEST_QUESTION_ID}/"

        @pytest.mark.parametrize(
            ("bad_url"),
            [
                (
                    f"/explore/question_{TEST_QUESTION_ID}/thumb/BAD/{DISLIKED_ANSWER_ID}"
                ),
                (f"/explore/question_{TEST_QUESTION_ID}/thumb/up/{INVALID_ANSWER_ID}"),
            ],
        )
        def test_logged_user_bad_route(self, logged_client, bad_url):
            response = logged_client.get(bad_url)
            assert response.status_code == 404

        def test_unauthorized_response(self, client):
            response = client.get(f"/explore/question_{TEST_QUESTION_ID}/thumb/up/9")
            assert response.status_code == 401

    class TestThumbsView:
        @pytest.mark.parametrize(
            ("answer_id", "thumb_type", "like_val", "false_val"),
            [
                (DISLIKED_ANSWER_ID, "up", True, False),
                (LIKED_ANSWER_ID, "up", False, False),
                (DISLIKED_ANSWER_ID, "down", False, False),
                (LIKED_ANSWER_ID, "down", False, True),
            ],
        )
        def test_thumbs_view(
            self, logged_client, answer_id, thumb_type, like_val, false_val
        ):
            response = logged_client.get(
                f"/explore/question_{TEST_QUESTION_ID}/thumb/{thumb_type}/{answer_id}"
            )
            response = logged_client.get(response.url)
            answers_tuples = response.context["answers_tuples"]
            for answer, like, dislike in answers_tuples:
                if answer.id == answer_id:
                    assert like == like_val and dislike == false_val

        def test_like_dislike_fields_update(self, answers, logged_client):
            answer_id1 = answers[0].id
            answer_id2 = answers[1].id
            assert answers[0].likes.exists() is False
            assert answers[1].dislikes.exists() is False
            logged_client.get(
                f"/explore/question_{TEST_QUESTION_ID}/thumb/up/{answer_id1}"
            )
            response = logged_client.get(
                f"/explore/question_{TEST_QUESTION_ID}/thumb/down/{answer_id2}"
            )
            profile = response.wsgi_request.profile
            assert profile in answers[0].likes.all()
            assert profile in answers[1].dislikes.all()
