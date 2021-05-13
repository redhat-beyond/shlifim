import pytest


@pytest.mark.django_db
class TestLogin:
    @pytest.fixture
    def valid_user_details(self):
        return {"username": "Lior", "password": "LiorLior"}

    @pytest.fixture
    def invalid_user_details(self):
        return {"username": "Lior12", "password": "LiorLior"}

    def test_get_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def test_success_login_post_redirect(self, client, valid_user_details):
        response = client.post('/login/', valid_user_details)
        assert response.status_code == 302  # redirect
        assert response.url == '/'

    def test_login(self, client, valid_user_details):
        client.logout()
        response = client.get('/')
        assert not response.wsgi_request.user.is_authenticated  # logged out
        client.post('/login/', valid_user_details)
        response = client.get('/')
        assert response.wsgi_request.user.is_authenticated  # successfully logged in

    def test_unsuccessful_login_post_not_redirect(self, client, invalid_user_details):
        response = client.post('/login/', invalid_user_details)
        assert response.status_code == 200  # not redirected

    def test_unsuccessful_login_post_message(self, client, invalid_user_details):
        response = client.post('/login/', invalid_user_details)
        assert "Please enter a correct username and password" in str(response.content)

    def test_authenticated_user_view(self, client, valid_user_details):
        client.login(username=valid_user_details['username'], password=valid_user_details['password'])
        response = client.get('/')
        assert "Login" not in str(response.content)
        assert "Logout" in str(response.content)

    @pytest.mark.parametrize(('next'), [('about'), ('explore'), ('tags')])
    def test_redirection_to_last_page_url(self, client, next, valid_user_details):
        response = client.post('/login/?next=/{0}/'.format(next), valid_user_details)
        assert response.url == '/{0}/'.format(next)
