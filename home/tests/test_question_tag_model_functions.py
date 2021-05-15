import pytest
from home.models import Tag, Question_Tag


class TestQuestionTagModelFunctions:
    @pytest.mark.django_db
    def test_add_tags_to_question(self, question_test_data):
        test_tags = ['test_tag_1', 'test_tag_2', 'test_tag_3']
        question_test_data.add_tags_to_question(test_tags)

        assert list(question_test_data.tags.values()) == [{'id': 21, 'tag_name': 'test_tag_1'},
                                                          {'id': 22, 'tag_name': 'test_tag_2'},
                                                          {'id': 23, 'tag_name': 'test_tag_3'}]

    @pytest.mark.django_db
    def test_field_questions_in_tag(self, question_tag_test_data):
        assert question_tag_test_data.questions.values().count() == 1

    @pytest.mark.django_db
    def test_question_tag_table(self, question_test_data, question_tag_test_data):
        assert Question_Tag.objects.filter(question=question_test_data, tag=question_tag_test_data).exists()

    @pytest.mark.django_db
    def test_add_tags_to_question_one_new_input(self, question_test_data, question_tag_test_data):
        question_test_data.add_tags_to_question(['test_tag_2', 'test_tag_3'])
        assert question_test_data.tags.values().count() == 2

    @pytest.mark.django_db
    def test_tags_feed_no_parameters(self):
        assert Tag.tags_feed().count() == 20

    @pytest.mark.django_db
    def test_tags_feed_with_test_tag(self, tag_test_data):
        assert tag_test_data.tags_feed().count() == 21

    @pytest.mark.django_db
    def test_tags_feed_with_filter(self, tag_test_data):
        assert Tag.tags_feed('_t').count() == 1

    @pytest.mark.django_db
    def test_tags_feed_after_delete(self, tag_test_data):
        Tag.objects.filter(tag_name='test_tag_1').delete()
        assert Tag.tags_feed().count() == 20

    @pytest.mark.django_db
    def test_tags_feed_no_result(self):
        assert Tag.tags_feed('testtesttesttest').count() == 0

    @pytest.fixture
    def tag_test_data(self):
        tag = Tag(tag_name='test_tag_1')
        tag.save()
        return tag

    @pytest.fixture
    def question_tag_test_data(self, question_test_data):
        test_tag = Tag()
        test_tag.tag_name = 'test_tag_2'
        test_tag.save()
        new_pair = Question_Tag()
        new_pair.question = question_test_data
        new_pair.tag = test_tag
        new_pair.save()
        return test_tag
