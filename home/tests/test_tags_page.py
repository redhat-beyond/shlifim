import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.db.models.query import QuerySet


class TestTagsPage:
    @pytest.mark.django_db
    def test_tags_page_url(self, tags_response):
        assert tags_response.status_code == 200

    @pytest.mark.django_db
    def test_tags_page_return_type(self, tags_response):
        assert isinstance(tags_response.context['tags'], QuerySet)

    @pytest.mark.django_db
    def test_tags_page_template(self, tags_response):
        assertTemplateUsed(tags_response, 'home/tags.html')

    @pytest.fixture
    def tags_response(self, client):
        url = reverse('tags')
        response = client.get(url)
        return response

    @pytest.mark.django_db
    @pytest.mark.parametrize(('search, included'), [
        ('a', '<Tag: Bagrut_Exam>'),
        ('5', '<Tag: 5th_Grade>'),
        ('abc', '[]'),
        ('Pit', '<Tag: Pitagoras>'),
        ])
    def test_tags_page_with_search(self, client, search, included):
        response = client.get('/tags/?q=' + search)
        assert response.status_code == 200
        assert included in str(response.context['tags'])
