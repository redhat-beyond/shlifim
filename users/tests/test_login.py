import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
class TestLogin:
    landing_page_url = reverse("landing-page")
    login_url = reverse("login")

    @pytest.fixture
    def invalid_user_details(self):
        return {"username": "Lior12", "password": "LiorLior"}

    def test_get_login_page(self, client):
        response = client.get(self.login_url)
        assert response.status_code == 200

    def test_success_login_post_redirect(self, client, valid_user_details):
        response = client.post(self.login_url, valid_user_details)
        assert response.status_code == 302  # redirect
        assert response.url == self.landing_page_url

    def test_login(self, client, valid_user_details):
        client.logout()
        response = client.get(self.landing_page_url)
        assert not response.wsgi_request.user.is_authenticated  # logged out
        client.post(self.login_url, valid_user_details)
        response = client.get(self.landing_page_url)
        assert response.wsgi_request.user.is_authenticated  # successfully logged in

    def test_unsuccessful_login_post_not_redirect(self, client, invalid_user_details):
        response = client.post(self.login_url, invalid_user_details)
        assert response.status_code == 200  # not redirected

    def test_unsuccessful_login_post_message(self, client, invalid_user_details):
        response = client.post(self.login_url, invalid_user_details)
        assert "Please enter a correct username and password" in str(response.content)

    def test_authenticated_user_view(self, client, valid_user_details):
        user = User.objects.get(username=valid_user_details["username"])
        client.force_login(user)
        response = client.get(self.landing_page_url)
        assert "Login" not in str(response.content)
        assert "Logout" in str(response.content)

    @pytest.mark.parametrize(("next"), [("about"), ("explore"), ("tags")])
    def test_redirection_to_last_page_url(self, client, next, valid_user_details):
        response = client.post(
            "/users/login?next=/{0}/".format(next), valid_user_details
        )
        assert response.url == "/{0}/".format(next)
