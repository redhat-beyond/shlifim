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

    def clean_sub_subject(self):
        subject = self.cleaned_data.get("subject")
        sub_subject = self.cleaned_data.get("sub_subject")
        if sub_subject and sub_subject not in subject.sub_subject_set.all():
            raise forms.ValidationError("The sub-subject doesn't match the subject")
        else:
            return sub_subject


class CommentForm(forms.ModelForm):
    content = RichTextBleachField(default="")

    class Meta:
        model = Answer
        fields = ("content",)
