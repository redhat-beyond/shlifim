import pytest
from home.models import Question
from django.urls import reverse
from django.test import RequestFactory
from home.views import QuestionsListView
from django.db.models import Count


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

    class testExplorePageSorting:
        @pytest.fixture
        def factory(self):
            return RequestFactory()

        @pytest.mark.django_db
        def test_explore_page_sort_by_answers_num(self, factory):
            requested_result = Question.objects.all().annotate(answers_num=Count('answer')).order_by('-answers_num')

            url = reverse('explore-page')
            request = factory.get(url, {'order_by': 'answersNum'})
            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert list(view.get_queryset()) == list(requested_result)

        @pytest.mark.django_db
        def test_explore_page_sort_by_publish_date(self, factory):
            requested_result = Question.objects.all().order_by("-publish_date")

            url = reverse('explore-page')
            request = factory.get(url, {'order_by': '-publish_date'})
            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert list(view.get_queryset()) == list(requested_result)
