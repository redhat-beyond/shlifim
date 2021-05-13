import pytest


@pytest.mark.django_db
def test_default_params_profile(profile):
    assert profile.user.id >= 0  # check if user saved successfully and get an id
    assert profile.gender == 'U'  # default gender is U
    assert profile.is_blocked is False
