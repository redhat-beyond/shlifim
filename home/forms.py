from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Answer, Gender
from .RichTextBleachField import RichTextBleachField


class QuestionForm(forms.ModelForm):
    tags_ = forms.CharField(max_length=110, min_length=0, required=False)

    class Meta:
        model = Question
        fields = ('title', 'subject', 'sub_subject', 'grade', 'book', 'book_page', 'tags_', 'content')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    gender = forms.CharField(label='Gender', widget=forms.Select(choices=Gender.choices), initial='U')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'password1', 'password2', )


class CommentForm(forms.ModelForm):
    content = RichTextBleachField(blank=True, null=True)

    class Meta:
        model = Answer
        fields = ('content',)
