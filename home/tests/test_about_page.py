import pytest
from django.urls import reverse


class TestAboutPage:
    @pytest.mark.django_db
    @pytest.fixture
    def about_page_response(self, client):
        url = reverse("about")
        response = client.get(url)
        return response

    def test_about_page_url(self, about_page_response):
        assert about_page_response.status_code == 200

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ("link"),
        [
            ("https://github.com/beyond-io/shlifim"),
            ("mailto:shlifimcontact@gmail.com"),
            ("https://github.com/avivz450"),
            ("https://www.linkedin.com/in/aviv-zafrani-aa4351180/"),
            ("https://github.com/danitLevi"),
            ("https://www.linkedin.com/in/danit-levi/"),
            ("https://github.com/idokk1"),
            ("https://www.linkedin.com/in/ido-kahlon-61bbb01aa/"),
            ("https://github.com/rebeccaTubman"),
            ("https://www.linkedin.com/in/rebecca-tubman/"),
            ("https://github.com/liornoy"),
            ("https://www.linkedin.com/in/lior-noy/"),
        ],
    )
    def test_links_in_about_page(self, about_page_response, link):
        char_content = about_page_response.content.decode(about_page_response.charset)
        assert '<a href="{0}"'.format(link) in char_content
