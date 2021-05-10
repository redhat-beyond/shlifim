import pytest
from home.models import Question
from django.urls import reverse


class TestExplorePage:
    class TestModelFunctions:

        @pytest.mark.parametrize("question_id, expected_result", [
            ("1", 5),
            ("2", 1),
            ("3", 0),
            ("4", 0),
        ])
        @pytest.mark.django_db
        def test_answers_num_func(self, question_id, expected_result):
            question = Question.objects.get(id=question_id)
            answers_num = question.get_answers_num()
            assert answers_num == expected_result

    class TestExplorePageView:

        @pytest.mark.django_db
        @pytest.fixture
        def explore_page_response(self, client):
            url = reverse('explore-page')
            response = client.get(url)
            return response

        @pytest.mark.django_db
        def test_explore_page_response(self, explore_page_response):
            assert explore_page_response.status_code == 200
            assert explore_page_response.templates[0].name == "home/explore.html"

            questions = Question.objects.all()
            assert set(explore_page_response.context['questions']) == set(questions)

        @pytest.mark.django_db
        def test_new_question_btn_in_explore_page(self, explore_page_response):
            char_content = explore_page_response.content.decode(explore_page_response.charset)
            assert '<a href="%s"' % reverse("new_question") in char_content
