import pytest
from home.models import Question
from django.urls import reverse


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

            questions = Question.objects.all()
            assert set(explore_page_response.context['questions']) == set(questions)

        @pytest.mark.django_db
        def test_new_question_btn_in_explore_page(self, explore_page_response):
            char_content = explore_page_response.content.decode(explore_page_response.charset)
            assert '<a href="%s"' % reverse("new_question") in char_content

    class TestTagsFilter:

        @pytest.mark.parametrize(('tag_name', 'wanted_questions_ids_lst'), [
            ("Bagrut_Exam", [8, 2, 14]),
            ("5th_Grade", [4, 3, 1]),
            ("Pitagoras", [8, 3, 1]),
        ])
        @pytest.mark.django_db
        def test_questions_filter_by_tag(self, client, tag_name, wanted_questions_ids_lst):
            url = f'/explore/?tag={tag_name}'
            response = client.get(url)

            requested_questions_ids = response.context['questions'].values_list('id', flat=True)
            assert wanted_questions_ids_lst == list(requested_questions_ids)

        @pytest.mark.parametrize('tag_name', [
            "Bagrut_Exam",
            "5th_Grade",
            "Pitagoras",
        ])
        @pytest.mark.django_db
        def test_context_with_tags(self, client, tag_name):
            url = f'/explore/?tag={tag_name}'
            response = client.get(url)

            requested_tag = response.context['tag']
            assert requested_tag == tag_name

        @pytest.mark.django_db
        def test_context_no_tag_parameter(self, explore_page_response):
            requested_tag = explore_page_response.context['tag']
            assert requested_tag is None

        @pytest.mark.parametrize('invalid_tag_name', [
            "AAA",
            "ERORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",

        ])
        @pytest.mark.django_db
        def test_invalid_tag(self, client, invalid_tag_name):
            url = f'/explore/?tag={invalid_tag_name}'
            response = client.get(url)
            assert response.status_code == 404
