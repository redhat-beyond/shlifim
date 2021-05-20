from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Question, Tag, Profile, Answer
from django.views.generic.list import ListView
from .forms import QuestionForm, SignUpForm, CommentForm
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


def about(request):
    return render(request, 'home/about.html')


def landingpage(request):
    return render(request, 'home/landingpage.html')


def display_question_page(request, pk):
    form = CommentForm(request.POST)
    question = get_object_or_404(Question, id=pk)
    sort_answer_by = request.GET.get("sortanswersby", "")
    context = {
        "question": question,
        "answers_tuples": Answer.get_answers_tuples(question, sort_answer_by, request.profile),
        "answersCount": question.answer_set.count(),
        "tags": question.tags.values(),
        "title": question.get_question_title(),
        "is_user_logged_in": request.user.is_authenticated,
        "form": form
    }
    if request.method == 'POST':
        if form.is_valid():
            if (request.profile is None):
                return HttpResponse('Unauthorized', status=401)
            else:
                form.instance.profile = request.profile
                form.instance.question = question
                form.save()
            return redirect(reverse("question-detail", kwargs={
                'pk': question.pk
            }))
    return render(request, 'home/question_detail.html', context)


def thumbs(request, **kwargs):
    if request.user.is_authenticated:
        question_id = kwargs['question_pk']
        answer = get_object_or_404(Answer, pk=kwargs['answer_pk'])
        if kwargs['string'] == 'up':
            answer.handle_thumb_up(request.profile)
        elif kwargs['string'] == 'down':
            answer.handle_thumb_down(request.profile)
        else:
            raise Http404
        return redirect('question-detail', question_id)
    else:
        return HttpResponse('Unauthorized', status=401)


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
