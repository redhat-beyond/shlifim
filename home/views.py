from django.shortcuts import render, get_object_or_404
from .models import Question, Tag
from django.views.generic.list import ListView
from .forms import QuestionForm


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


def displayQuestion(request, **kwargs):
    question = get_object_or_404(Question, id=kwargs['pk'])
    sortAnsBy = request.GET["sortanswersby"] if 'sortanswersby' in request.GET else ''
    context = {
        "question": question,
        "answers": question.get_answers_feed(sortAnsBy),
        "answersCount": question.answer_set.count(),
        "tags": question.tags.values(),
        "title": question.get_question_title()
    }
    return render(request, 'home/question_detail.html', context)


def tags(request):
    if 'q' in request.GET:
        search = request.GET['q']
        tags = Tag.tags_feed(search)
    else:
        tags = Tag.tags_feed()
    return render(request, 'home/tags.html', {'tags': tags})


def new_question(request):
    form = QuestionForm
    if request.method == 'POST':
        questForm = QuestionForm(request.POST)
        if questForm.is_valid():
            questForm = questForm.save(commit=False)
            questForm.profile = request.profile
            questForm.save()
    return render(request, 'home/questions/new_question.html', {'form': form, 'title': 'New Question'})


class QuestionsListView(ListView):
    model = Question
    template_name = 'home/explore.html'
    context_object_name = 'questions'
    ordering = ['-publish_date']
