from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    UNSPECIFIED = "U", "Unspecified"


class Profile(models.Model):
    """
    Profile will be used as the base user in the Shlifim website.
    Profile is an extention to the imported 'User' from 'django.contrib.auth.models'.
    Imported Fields:
    username - Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
    password - Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password).
               Raw passwords can be arbitrarily long and can contain any character.
    date_joined - A datetime designating when the account was created. Is set to the current date/time by default
        when the account is created.
    email - Email address.
    is_superuser - Boolean. Designates that this user has all permissions without explicitly assigning them.
    Added Fields:
    gender - Default gender is set to 'Unspecified', A user can choose to specifie its gender to Male/Female.
    is blocked - Boolean. Designates that this user won't be able to login until an admin unblockes him.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED
    )
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return "{self.user.username}".format(self=self)

    @classmethod
    def create(cls, username, password, email, gender="U", is_blocked=False):
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        profile = cls(user=user, gender=gender, is_blocked=is_blocked)
        profile.save()
        return profile

    @classmethod
    def profiles_feed(cls):
        return cls.objects.all()
