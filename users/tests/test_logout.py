import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestLogout:
    landing_page_url = reverse("landing-page")
    logout_url = reverse("logout")

    def test_status_code(self, client):
        response = client.get(self.logout_url)
        assert response.status_code == 302  # redirected

    def test_redirection_default_url(self, client):
        response = client.get(self.logout_url)
        assert response.url == self.landing_page_url  # redirected to home page.

    def test_logout(self, client, authenticated_user):
        response = client.get(self.landing_page_url)
        assert response.wsgi_request.user.is_authenticated  # successfully logged in
        response = client.get(self.logout_url)
        assert (
            not response.wsgi_request.user.is_authenticated
        )  # successfully logged out

    def test_unauthenticated_user_view(self, client):
        response = client.get(self.landing_page_url)
        assert "Login" in str(response.content)
        assert "Logout" not in str(response.content)

    @pytest.mark.parametrize(("next"), [("about"), ("explore"), ("tags")])
    def test_redirection_to_last_page_url(self, client, request, next):
        response = client.get("/users/logout?next=/{0}/".format(next))
        assert response.url == "/{0}/".format(next)
