from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Tag, Profile
from django.views.generic.list import ListView
from .forms import QuestionForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


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


@login_required(login_url='/login/')
def new_question(request):
    form = QuestionForm
    if request.method == 'POST':
        questForm = QuestionForm(request.POST)
        if questForm.is_valid():
            questForm = questForm.save(commit=False)
            questForm.profile = request.profile
            questForm.save()
            return redirect('question-detail', questForm.id)
    return render(request, 'home/questions/new_question.html', {'form': form, 'title': 'New Question'})


class QuestionsListView(ListView):
    model = Question
    template_name = 'home/explore.html'
    ordering = ['-publish_date']

    def get_context_data(self, **kwargs):
        requested_tag_name = self.request.GET.get('tag', None)

        if requested_tag_name:
            requested_tag_obj = get_object_or_404(Tag, tag_name=requested_tag_name)
            items_set = requested_tag_obj.question_set.all()
        else:
            items_set = Question.objects.all()

        context = {
            'tag': requested_tag_name,
            'questions': items_set,
        }

        context.update(kwargs)
        return super().get_context_data(**context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user.save()
            profile = Profile(user=user)
            user = authenticate(username=user.username, password=raw_password)
            profile.gender = form.cleaned_data.get('gender')
            profile.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})
