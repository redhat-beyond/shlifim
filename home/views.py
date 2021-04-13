from django.shortcuts import render
from .models import Question


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


def displayQuestion(request, **kwargs):
    question = Question.objects.all().get(id=kwargs['pk'])
    sortAnsBy = request.GET["sortanswersby"] if 'sortanswersby' in request.GET else ''
    context = {
        "question": question,
        "answers": question.get_answers_feed(sortAnsBy),
        "answersCount": question.answer_set.count(),
        "tags": question.tags.values(),
        "title": question.get_question_title()
    }
    return render(request, 'home/question_detail.html', context)
