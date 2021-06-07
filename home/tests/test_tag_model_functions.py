import pytest
from home.models import Tag


@pytest.mark.django_db
class TestTagModelFunctions:
    @pytest.mark.parametrize(
        "valid_tags",
        [
            ([]),
            (["beyond_01"]),
            (["beyond_01", "beyond_02"]),
            (["beyond_01", "beyond_02", "beyond_03"]),
            (["beyond_01", "beyond_02", "beyond_03", "beyond_04"]),
            (["beyond_01", "beyond_02", "beyond_03", "beyond_04", "beyond_05"]),
        ],
    )
    def test_check_tag_array_valid_data(self, valid_tags):
        assert Tag.check_tag_array(valid_tags) is True

    @pytest.mark.parametrize(
        "invalid_tags",
        [
            (["1"]),
            (["beyond_01beyond_01beyond_01"]),
            (
                [
                    "beyond_01",
                    "beyond_02",
                    "beyond_03",
                    "beyond_04",
                    "beyond_05",
                    "beyond_06",
                ]
            ),
        ],
    )
    def test_check_tag_array_invalid_data(self, invalid_tags):
        assert Tag.check_tag_array(invalid_tags) is False

    def test_tags_feed_no_parameters(self):
        assert Tag.tags_feed().count() == 20

    def test_tags_feed_with_test_tag(self, tag_test_data):
        assert tag_test_data.tags_feed().count() == 21

    def test_tags_feed_with_filter(self, tag_test_data):
        assert Tag.tags_feed("_t").count() == 1

    def test_tags_feed_after_delete(self, tag_test_data):
        Tag.objects.filter(tag_name="test_tag_1").delete()
        assert Tag.tags_feed().count() == 20

    def test_tags_feed_no_result(self):
        assert Tag.tags_feed("testtesttesttest").count() == 0

    @pytest.fixture
    def tag_test_data(self):
        tag = Tag(tag_name="test_tag_1")
        tag.save()
        return tag
