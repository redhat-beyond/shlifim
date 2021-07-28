from django.urls import path
from .views import (
    about,
    landingpage,
    tags,
    new_question,
    thumbs,
    display_question_page,
    DeleteQuestionView,
    QuestionsListView,
)

urlpatterns = [
    path("about/", about, name="about"),
    path("", landingpage, name="landing-page"),
    path("tags/", tags, name="tags"),
    path("explore/", QuestionsListView.as_view(), name="explore-page"),
    path("explore/new_question", new_question, name="new-question"),
    path(
        "explore/question_<int:question_pk>/thumb/<string>/<int:answer_pk>",
        thumbs,
    ),
    path(
        "explore/question_<int:pk>/",
        display_question_page,
        name="question-detail",
    ),
    path(
        "explore/question_<int:pk>/delete",
        DeleteQuestionView.as_view(),
        name="question-delete",
    ),
]
