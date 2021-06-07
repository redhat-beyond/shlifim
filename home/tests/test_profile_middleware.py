import pytest
from home.profile_middleware import ProfileMiddleware
from unittest.mock import Mock
from django.contrib.auth.models import User
from home.models import Profile


class TestProfileMiddleware:
    @pytest.mark.django_db
    class LoggedOutUserMock:
        is_authenticated = False

        def test_process_request_with_logged_in_user(self):
            logged_in_user = User.objects.latest("id")
            pm = ProfileMiddleware("response")
            assert logged_in_user.is_authenticated is True

            request_mock = Mock(user=User.objects.latest("id"))
            pm.process_view(request_mock, None, None, None)
            assert (
                request_mock.profile
                == Profile.objects.filter(user=logged_in_user).first()
            )

        def test_process_request_with_logged_out_user(self):
            logged_out_user = self.LoggedOutUserMock()
            pm = ProfileMiddleware("response")
            assert logged_out_user.is_authenticated is False

            request_mock = Mock(user=self.LoggedOutUserMock())
            pm.process_view(request_mock, None, None, None)
            assert request_mock.profile is None
