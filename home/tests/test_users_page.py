import pytest
from pytest_django.asserts import assertTemplateUsed
from django.db.models.query import QuerySet
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(('user_id', 'expected'), [('1', 200), ('2', 200), ('BAD', 404), ('-50', 404)])
def test_url_status_code(client, user_id, expected):
    response = client.get(f'/users/{user_id}')
    assert response.status_code == expected


@pytest.mark.django_db
def test_view_context_and_template(client):
    response = client.get(reverse('user-page', args=[1]))
    assertTemplateUsed(response, 'home/user_page.html')
    assert str(response.context['profile']) == 'Rebecca'
    assert isinstance(response.context['user_questions'], QuerySet)
    assert isinstance(response.context['user_answers'], QuerySet)


@pytest.mark.django_db
def test_users_page(client):
    response = client.get(reverse('users'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'home/users.html')
    assert isinstance(response.context['profiles'], QuerySet)
