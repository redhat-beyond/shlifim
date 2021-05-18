import pytest


@pytest.mark.django_db
class TestLogout:
    def test_status_code(self, client):
        response = client.get('/logout/')
        assert response.status_code == 302  # redirected

    def test_redirection_default_url(self, client):
        response = client.get('/logout/')
        assert response.url == '/'  # redirected to home page.

    def test_logout(self, client, authenticated_user):
        response = client.get('/')
        assert response.wsgi_request.user.is_authenticated  # successfully logged in
        response = client.get('/logout/')
        assert not response.wsgi_request.user.is_authenticated   # successfully logged out

    def test_unauthenticated_user_view(self, client):
        response = client.get('/')
        assert "Login" in str(response.content)
        assert "Logout" not in str(response.content)

    @pytest.mark.parametrize(('next'), [('about'), ('explore'), ('tags')])
    def test_redirection_to_last_page_url(self, client, request, next):
        response = client.get('/logout/?next=/{0}/'.format(next))
        assert response.url == '/{0}/'.format(next)
