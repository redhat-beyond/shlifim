from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gender


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )
    gender = forms.CharField(
        label="Gender", widget=forms.Select(choices=Gender.choices), initial="U"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        registered_email_count = User.objects.filter(email=email).count()

        if email and registered_email_count > 0:
            raise forms.ValidationError(
                "This email address is already in use. Please supply a different email address."
            )
        return email
