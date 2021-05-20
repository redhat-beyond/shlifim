import pytest
import pytz
from home.models import Profile, Subject, Question, Grade
from pytest_django.asserts import assertTemplateUsed
from home.forms import QuestionForm
from datetime import datetime
from django.core.exceptions import ValidationError


class TestInsertQuestionFeature:
    class TestDatabaseInsertions:
        @pytest.fixture
        def question(self):
            return Question(profile=Profile.objects.first(),
                            title="Question in Math",
                            content='How much is it 1+1?',
                            subject=Subject.objects.first(),
                            grade=Grade.GRADE7)

        @pytest.mark.parametrize("valid_Input", [
            (10, 1, "Question in Math", 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), 1, 4, Grade.GRADE7, 1, 10, False),
            # User entered all the fields
            (10, 1, "Question in Math", "",
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), 1, 4, Grade.GRADE7, 1, 10, False),
            # User entered all the fields except content
            (11, 2, "Question in History", 'How many wars Israel had?',
             datetime(2022, 4, 7, 12, 59, 55, 4, tzinfo=pytz.UTC), 1, None, Grade.GRADE8, 2, 11, False),
            # User entered all the fields except Sub_Subject
            (11, 2, "Question in History", 'How many wars Israel had?',
             datetime(2022, 4, 7, 12, 59, 55, 4, tzinfo=pytz.UTC), 1, 4, Grade.GRADE8, None, 11, False),
            # User entered all the fields except Book
            (10, 1, "Question in Math", 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), 1, 4, Grade.GRADE7, 1, None, False),
            # User entered all the fields except Book page
        ])
        @pytest.mark.django_db
        def test_add_valid_question(self, valid_Input):
            question = Question(*valid_Input)
            question.save()

            assert Question.objects.filter(pk=question.id).exists()

        @pytest.mark.parametrize("invalid_Input, exception", [
            ((10, 3, None, 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), 1, 4, Grade.GRADE7, 1, 10, False), ValidationError),
            # User didn't enter title
            ((10, 1, "Question in Math", 'How much is it 1+1?', "",
             1, 4, Grade.GRADE7, 1, 10, False), ValidationError),
            # The question does not contain date
            ((10, 1, "Question in Math", 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), "", 4, Grade.GRADE7, 1, 10, False), ValidationError),
            # User didn't choose subject
            ((10, 1, "Question in Math", 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), 1, 4, "", 1, 10, False), ValidationError),
            # User did'nt choose grade
            ((10, 1, "Question in Math", 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC), 1, 4, Grade.GRADE7, 1, -10, False), ValidationError),
            # User chose negative book number
            ((10, 1, "Question in Math", 'How much is it 1+1?',
             datetime(2022, 4, 7, 12, 53, 29, 4, tzinfo=pytz.UTC),
             1, 4, Grade.GRADE7, 1, 99990, False), ValidationError),
            # User entered to high book number
        ])
        @pytest.mark.django_db
        def test_add_invalid_question(self, invalid_Input, exception):

            with pytest.raises(exception):
                assert Question(*invalid_Input).clean_fields()

        @pytest.mark.django_db
        def test_default_is_edited_is_false(self, question):

            assert question.is_edited is False

        @pytest.mark.django_db
        def test_default_book_page_is_none(self, question):

            assert question.book_page is None

        @pytest.mark.django_db
        def test_default_book_is_none(self, question):

            assert question.book is None

        @pytest.mark.django_db
        def test_default_sub_subject_is_none(self, question):

            assert question.sub_subject is None

    class TestViews:
        @pytest.mark.parametrize("valid_data", [
            ({'title': "Question in Math", 'subject': 1,
             'grade': Grade.GRADE7, 'tags_': ""}),
            # User entered all the required fields
            ({'title': "Question in Math", 'subject': 1,
             'grade': Grade.GRADE7, 'tags_': "beyond_01"}),
            # User entered all the required fields and one tag
            ({'title': "Question in Math", 'subject': 1,
             'grade': Grade.GRADE7, 'tags_': "beyond_01, beyond_02"}),
            # User entered all the required fields and two tags
            ({'title': "Question in Math", 'subject': 1, 'grade': Grade.GRADE7,
             'tags_': "beyond_01, beyond_02, beyond_03"}),
            # User entered all the required fields and three tags
            ({'title': "Question in Math", 'subject': 1, 'grade': Grade.GRADE7,
             'tags_': "beyond_01, beyond_02, beyond_03, beyond_04"}),
            # User entered all the required fields and four tags
            ({'title': "Question in Math", 'subject': 1, 'grade': Grade.GRADE7,
             'tags_': "beyond_01, beyond_02, beyond_03, beyond_04, beyond_05"}),
            # User entered all the required fields and five tags
            ({'title': "Question in Math",
              'subject': 1, 'content': 'How much is it 1+1?', 'grade': Grade.GRADE7, 'tags_': ""}),
            # User entered all the required fields and content
            ({'title': "Question in Math",
              'subject': 1, 'grade': Grade.GRADE7, 'sub-subject': 2, 'tags_': ""}),
            # User entered all the required fields and sub-subject
            ({'title': "Question in Math",
              'subject': 1, 'grade': Grade.GRADE7, 'book': 2, 'tags_': ""}),
            # User entered all the required fields and sub-subject and book
            ({'title': "Question in Math",
              'subject': 1, 'grade': Grade.GRADE7, 'book_page': 23, 'tags_': ""}),
            # User entered all the required fields and a valid book page
        ])
        @pytest.mark.django_db
        def test_post_valid_question_with_client(self, client, valid_data, authenticated_user):
            with pytest.raises(Question.DoesNotExist):
                assert Question.objects.get(title=valid_data["title"])

            response = client.post('/explore/new_question', data=valid_data)
            assert Question.objects.filter(title=valid_data["title"]).exists()
            assert response.status_code == 302
            question_id = Question.objects.get(title=valid_data["title"]).id
            assert response.url == "/explore/question_" + \
                str(question_id) + "/"

        @pytest.mark.parametrize("invalid_data", [
            ({'title': "Question in Math", 'content': 'How much is it 1+1?',
             'tags_': "", 'grade': Grade.GRADE7}),
            # User entered all the required fields except subject
            ({'title': "Question in Math",
             'content': 'How much is it 1+1?', 'tags_': "", 'subject': 1}),
            # User entered all the required fields except grade
            ({'title': "Question in Math", 'content': 'How much is it 1+1?',
             'tags_': "", 'subject': 1, 'book_page': -23}),
            # User entered all the required fields and a negative book page
            ({'title': "Question in Math", 'content': 'How much is it 1+1?',
             'tags_': "", 'subject': 1, 'book_page': 43343}),
            # User entered all the required fields and to high book page
            ({'title': "Question in Math", 'subject': 1, 'content': 'How much is it 1+1?',
             'tags_': "aaaaaaaaaaaaaaaaaaaaaaaa", 'grade': Grade.GRADE7}),
            # User entered all the required fields and invalid tags (more than 20 chars tag)
            ({'title': "Question in Math", 'subject': 1, 'content': 'How much is it 1+1?',
             'tags_': "a", 'grade': Grade.GRADE7}),
            # User entered all the required fields and invalid tags (1 char tag)
            ({'title': "Question in Math", 'subject': 1, 'content': 'How much is it 1+1?',
             'tags_': "beyond_01, beyond_02, beyond_03, beyond_04, beyond_05, beoynd_06", 'grade': Grade.GRADE7}),
            # User entered all the required fields and invalid tags (more than 5 tags)
        ])
        @pytest.mark.django_db
        def test_post_invalid_question_with_client(self, client, invalid_data, authenticated_user):
            response = client.post('/explore/new_question', data=invalid_data)
            assert response.status_code == 200

            with pytest.raises(Question.DoesNotExist):
                assert Question.objects.get(title=invalid_data["title"])

        @pytest.mark.django_db
        def test_post_question_without_title_with_client(self, client, authenticated_user):
            client.post('/explore/new_question', data={'content': 'How much is it 1+1?',
                                                       'subject': 1, 'grade': Grade.GRADE7})

            with pytest.raises(Question.DoesNotExist):
                assert Question.objects.get(content='How much is it 1+1?')

        @pytest.mark.django_db
        def test_question_form_and_template_displayed(self, client, authenticated_user):
            response = client.get('/explore/new_question')

            assert response.status_code == 200
            assert isinstance(response.context['form'], type(QuestionForm))
            assertTemplateUsed(response, 'home/questions/new_question.html')

        def test_redirection_user_logged_out(self, client):
            response = client.get('/explore/new_question')

            assert response.status_code == 302
            assert response.url == '/login/?next=/explore/new_question'

        @pytest.mark.django_db
        def test_valid_tags_not_removed_from_question(self, client, authenticated_user):
            data = {'title': "Question in Math",
                    'subject': 1, 'content': '<p>a</p>',
                    'grade': Grade.GRADE7, 'tags_': ""}
            client.post('/explore/new_question', data=data)
            question = Question.objects.filter(title=data["title"]).first()
            assert "<p>" in question.content

        @pytest.mark.django_db
        def test_invalid_tags_removed_from_question(self, client, authenticated_user):
            data = {'title': "Question in Math",
                    'subject': 1, 'content': '<script language = "javascript" > alert("You are PWNED!") </script>',
                    'grade': Grade.GRADE7, 'tags_': ""}
            client.post('/explore/new_question', data=data)
            question = Question.objects.filter(title=data["title"]).first()
            assert "<script>" not in question.content
