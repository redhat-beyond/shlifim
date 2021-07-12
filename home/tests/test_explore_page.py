import pytest
from home.models import Question
from django.urls import reverse


@pytest.mark.django_db
class TestExplorePage:
    @pytest.fixture
    def explore_page_response(self, client):
        url = reverse("explore-page")
        response = client.get(url)
        return response

    class TestModelFunctions:
        @pytest.mark.parametrize(
            "question_id, expected_result",
            [
                ("1", 5),
                ("2", 1),
                ("3", 0),
                ("4", 0),
            ],
        )
        def test_answers_num_func(self, question_id, expected_result):
            question = Question.objects.get(id=question_id)
            answers_num = question.get_answers_num()
            assert answers_num == expected_result

    class TestExplorePageView:
        def test_explore_page_response(self, explore_page_response):
            assert explore_page_response.status_code == 200
            assert explore_page_response.templates[0].name == "home/explore.html"

            questions = Question.objects.all()
            assert set(explore_page_response.context["questions"]) == set(questions)

        def test_new_question_btn_in_explore_page(self, explore_page_response):
            char_content = explore_page_response.content.decode(
                explore_page_response.charset
            )
            assert '<a href="%s"' % reverse("new-question") in char_content

    class TestTagsFilter:
        explore_page_url = reverse("explore-page")

        @pytest.mark.parametrize(
            ("tag_name", "wanted_questions_ids_lst"),
            [
                ("Bagrut_Exam", [2, 14]),
                ("5th_Grade", [8, 2]),
                ("Pitagoras", [8, 2]),
            ],
        )
        def test_questions_filter_by_tag(
            self, client, tag_name, wanted_questions_ids_lst
        ):
            url = reverse("explore-page")
            param_dict = {"tag": tag_name}
            response = client.get(url, param_dict)

            requested_questions_ids = response.context["questions"].values_list(
                "id", flat=True
            )
            assert wanted_questions_ids_lst == list(requested_questions_ids)

        @pytest.mark.parametrize(
            "tag_name",
            [
                "Bagrut_Exam",
                "5th_Grade",
                "Pitagoras",
            ],
        )
        def test_context_with_tags(self, client, tag_name):

            url = self.explore_page_url
            param_dict = {"tag": tag_name}
            response = client.get(url, param_dict)
            requested_tag = response.context["tag"]
            assert requested_tag == tag_name

        def test_context_no_tag_parameter(self, explore_page_response):
            requested_tag = explore_page_response.context["tag"]
            assert requested_tag is None

        @pytest.mark.parametrize(
            "invalid_tag_name",
            [
                "AAA",
                "ERORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
            ],
        )
        def test_invalid_tag(self, client, invalid_tag_name):
            url = self.explore_page_url
            param_dict = {"tag": invalid_tag_name}
            response = client.get(url, param_dict)
            assert response.status_code == 404

        @pytest.mark.parametrize("tag_name", ["#Pitagoras", "#Bagrut_Exam"])
        def test_explore_page_tags_view(self, explore_page_response, tag_name):
            assert tag_name in str(explore_page_response.content)
