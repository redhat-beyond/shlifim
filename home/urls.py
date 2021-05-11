from django.urls import path
from . import views
from .views import QuestionsListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.landingpage, name='landingpage'),
    path('explore/question_<int:pk>/', views.displayQuestion, name='question-detail'),
    path('tags/', views.tags, name='tags'),
    path('explore/', QuestionsListView.as_view(), name='explore-page'),
    path('explore/new_question', views.new_question, name='new_question'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login')
]
