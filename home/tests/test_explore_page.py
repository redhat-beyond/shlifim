import pytest
from django.urls import reverse
from home.models import Subject, Sub_Subject, Question, Grade, Book
from django.test import RequestFactory
from home.views import QuestionsListView


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

    class TestExplorePageFilter:

        @pytest.fixture
        def factory(self):
            return RequestFactory()

        @pytest.mark.django_db
        @pytest.mark.parametrize("objId", [1, 2, 3])
        def test_explore_page_filter_by_subject(self, factory, objId):
            subject = Subject.objects.get(pk=objId)
            requested_result = Question.objects.all().filter(subject=subject)

            url = reverse('explore-page')
            request = factory.get(url, {'subject': objId})
            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert list(view.get_queryset()) == list(requested_result)

        @pytest.mark.django_db
        @pytest.mark.parametrize("objId", [1, 2, 3])
        def test_explore_page_filter_by_sub_subject(self, factory, objId):
            sub_subject = Sub_Subject.objects.get(pk=objId)
            requested_result = Question.objects.all().filter(sub_subject=sub_subject)

            url = reverse('explore-page')
            request = factory.get(url, {'sub_subject': objId})
            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert list(view.get_queryset()) == list(requested_result)

        @pytest.mark.parametrize("objId", [1, 2, 3])
        @pytest.mark.django_db
        def test_explore_page_filter_by_book(self, factory, objId):
            book = Book.objects.get(pk=objId)
            requested_result = Question.objects.all().filter(book=book)

            url = reverse('explore-page')
            request = factory.get(url, {'book': objId})
            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert list(view.get_queryset()) == list(requested_result)

        @pytest.mark.django_db
        def test_explore_page_filter_by_grade(self, factory):
            grade = Grade.GRADE7
            requested_result = Question.objects.all().filter(grade=grade)

            url = reverse('explore-page')
            request = factory.get(url, {'grade': 7})
            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert list(view.get_queryset()) == list(requested_result)

        @pytest.mark.django_db
        def test_explore_page_filter_zero_results(self, factory):
            subject = Subject.objects.get(pk=1)
            grade = Grade.GRADE11
            requested_result = Question.objects.all().filter(subject=subject).filter(grade=grade)

            url = reverse('explore-page')
            request = factory.get(url, {'subject': 1, 'grade': 11})

            view = QuestionsListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            assert len(list(view.get_queryset())) == len(list(requested_result)) == 0
