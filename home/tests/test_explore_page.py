import pytest
from home.models import Question
from django.urls import reverse
import math


class TestExplorePage:

    @pytest.mark.django_db
    @pytest.fixture
    def explore_page_response(self, client):
        url = reverse('explore-page')
        response = client.get(url)
        return response

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
        def test_explore_page_response(self, explore_page_response):
            assert explore_page_response.status_code == 200
            assert explore_page_response.templates[0].name == "home/explore.html"

    class TestExplorePagePaginator:
        @pytest.mark.django_db
        def test_explore_page_is_paginated(self, explore_page_response):
            assert (explore_page_response.context['is_paginated'] is True)

        @pytest.mark.parametrize("items_per_page", [
            5,
            10,
            15,
            20
        ])
        @pytest.mark.django_db
        def test_explore_page_items_per_page(self, items_per_page, client):
            # assert all questions appears in the explore page and corresponding the selected "items_per_page" .
            questions = list(Question.objects.all())

            last_page = math.ceil(len(questions) / items_per_page)
            curr_page = 1
            for i in range(0, len(questions), items_per_page):
                response = client.get(
                    reverse('explore-page') + '?paginate_by=' + str(items_per_page) + '&page=' + str(curr_page))
                response_questions = list(response.context['questions'])
                requested_questions = questions[i:i + items_per_page]

                assert (response_questions == requested_questions)

                if curr_page != last_page:
                    assert (len(response_questions) == items_per_page)
                    curr_page += 1
                else:
                    assert (len(response_questions) == len(questions) % items_per_page)
