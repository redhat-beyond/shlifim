import pytest
import pytz
from home.models import Profile, Question, Answer
from django.urls import reverse
from django.db.models.query import QuerySet
from datetime import datetime


class TestDisplayQuestionFeature:
    class TestAnswersManipulations:
        @pytest.fixture
        def answers(self):
            profile = Profile.objects.first()
            question = Question.objects.get(id=3)
            ans1 = Answer(profile=profile, question=question, content='Answer 1',
                          publish_date=datetime(2021, 4, 1, tzinfo=pytz.UTC),
                          likes_count=1, dislikes_count=0, is_edited=False)
            ans2 = Answer(profile=profile, question=question, content='Answer 2',
                          publish_date=datetime(2021, 4, 2, tzinfo=pytz.UTC),
                          likes_count=0, dislikes_count=0, is_edited=False)
            ans1.save()
            ans2.save()
            return [ans1, ans2]

        @pytest.mark.django_db
        def test_thumb_up_answer(self, answers):
            """
            thumb_up_answer(answer_id) increase the thumbs up field of an answer by one
            """
            prev_thumb_val = answers[0].likes_count
            answers[0].thumb_up_answer()
            assert(prev_thumb_val == answers[0].likes_count - 1)

        @pytest.mark.django_db
        def test_thumb_down_answer(self, answers):
            """
            thumb_down_answer(answer_id) increase the thumbs down field of an answer by one
            """
            prev_thumb_val = answers[0].dislikes_count
            answers[0].thumb_down_answer()
            assert(prev_thumb_val == answers[0].dislikes_count - 1)

        @pytest.mark.django_db
        def test_set_is_edited(self, answers):
            """
            Tests functionality of set_is_edited
            """
            prev_is_edited_val = answers[0].is_edited
            answers[0].set_is_edited(not prev_is_edited_val)
            assert(prev_is_edited_val != answers[0].is_edited)

        @pytest.mark.django_db
        @pytest.mark.parametrize(('filterType, expected'), [('date', 'Answer 2'), ('votes', 'Answer 1')])
        def test_answers_feed(self, filterType, expected, answers):
            """
            Tests if get_answers_feed returns queryset of all the answers of
            question number 3 sorted by votes or answers
            """
            question = Question.objects.get(id=3)
            answers_feed = question.get_answers_feed(filterType)
            assert isinstance(answers_feed, QuerySet)
            assert answers_feed[0].content == expected

    class TestQuestionRelatedMethods:
        @pytest.mark.django_db
        def test_get_question_title(self):
            """
            get_question_title(question_id) returns a string for question
            should return question subject and question title
            """
            question = Question.objects.get(id=1)
            assert(question.get_question_title() == "Math-question from math course")

    class TestHTMLRelated:
        @pytest.mark.django_db
        @pytest.fixture
        def response(self, client):
            url = reverse('question-detail', args=[14])
            response = client.get(url)
            return response

        @pytest.mark.django_db
        def test_display_question_page_url(self, response):
            """
            This test checks the returned status for routing to display-question feature
            """
            assert response.status_code == 200

        @pytest.mark.django_db
        def test_template_name(self, response):
            assert response.templates[0].name == "home/question_detail.html"

        @pytest.mark.django_db
        def test_response_context(self, response):
            '''
            Testing if the context passed to the view contains the right contents
            '''
            expectedPairs = [
                ('question', 'Question #14 : g forwards, it was even later than ( 28/04/2021 23:14 )'),
                ('answers', '<QuerySet [<Answer: Answer B>, <Answer: Answer A>,\
 <Answer: Popular Answer>, <Answer: Old Answer>]>'),
                ('answersCount', '4'),
                ('tags', '<QuerySet [{\'id\': 3, \'tag_name\': \'Bagrut_Exam\'}, \
{\'id\': 4, \'tag_name\': \'Hebrew\'}, {\'id\': 8, \'tag_name\': \'java\'}, \
{\'id\': 13, \'tag_name\': \'all_my_sons\'}]>'),
                ('title', 'History-g forwards, it was even later than')
                ]
            for check, expected in expectedPairs:
                assert str(response.context[check]) == expected

        @pytest.mark.parametrize(('filterType, expected'), [('date', 'Answer B'), ('votes', 'Popular Answer')])
        @pytest.mark.django_db
        def test_sorting_answers(self, client, filterType, expected):
            url = f'/explore/question_14/?sortanswersby={filterType}'
            response = client.get(url)
            answer = response.context['answers'].first()
            assert str(answer.content) == expected

        @pytest.mark.django_db
        def test_invalid_question_url(self, client):
            url = reverse('question-detail', args=[Question.objects.count()+1])
            response = client.get(url)
            assert response.status_code == 404

        @pytest.mark.django_db
        def test_invalid_answersort_url(self, client):
            url = '/explore/question_1/?sortanswersby=BAD'
            response = client.get(url)
            assert response.status_code == 404
