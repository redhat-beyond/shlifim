from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import QuestionsListView

urlpatterns = [
    path("about/", views.about, name="about"),
    path("", views.landingpage, name="landing-page"),
    path("tags/", views.tags, name="tags"),
    path("explore/", QuestionsListView.as_view(), name="explore-page"),
    path("explore/new_question", views.new_question, name="new-question"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="home/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
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
    path("users/<int:pk>", views.user_page, name="user-page"),
    path("users", views.users, name="users"),
]
