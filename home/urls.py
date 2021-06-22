from django.urls import path
from . import views
from .views import QuestionsListView

urlpatterns = [
    path("about/", views.about, name="about"),
    path("", views.landingpage, name="landing-page"),
    path("tags/", views.tags, name="tags"),
    path("explore/", QuestionsListView.as_view(), name="explore-page"),
    path("explore/new_question", views.new_question, name="new-question"),
    path(
        "explore/question_<int:question_pk>/thumb/<string>/<int:answer_pk>",
        views.thumbs,
    ),
    path(
        "explore/question_<int:pk>/",
        views.display_question_page,
        name="question-detail",
    ),
    path(
        "explore/question_<int:pk>/delete",
        views.DeleteQuestionView.as_view(),
        name="question-delete",
    ),
]
