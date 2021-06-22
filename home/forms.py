from django import forms
from .models import Question, Answer
from .RichTextBleachField import RichTextBleachField


class QuestionForm(forms.ModelForm):
    tags_ = forms.CharField(max_length=110, min_length=0, required=False)

    class Meta:
        model = Question
        fields = (
            "title",
            "subject",
            "sub_subject",
            "grade",
            "book",
            "book_page",
            "tags_",
            "content",
        )


class CommentForm(forms.ModelForm):
    content = RichTextBleachField(default="")

    class Meta:
        model = Answer
        fields = ("content",)
