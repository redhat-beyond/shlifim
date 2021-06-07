from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Question, Tag, Profile, Answer
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from .forms import QuestionForm, SignUpForm, CommentForm
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy


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
                if form.cleaned_data['content'] != "":
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


def users(request):
    profiles = Profile.profiles_feed()
    return render(request, 'home/users.html', {'profiles': profiles})


@login_required(login_url='/login/')
def new_question(request):
    form = QuestionForm
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            tags_array = [t.strip().lower() for t in question_form.cleaned_data['tags_'].split(',')]
            tags_status = Tag.check_tag_array(tags_array)
            if(not question_form.data['tags_'] or tags_status):
                question_form = question_form.save(commit=False)
                question_form.profile = request.profile
                question_form.save()
                if(tags_status):
                    questionInstane = Question.objects.get(id=question_form.id)
                    questionInstane.add_tags_to_question(tags_array)
                return redirect('question-detail', question_form.id)
            else:
                tags_error_msg = '''Invalid data.
             You may enter up to 5 tags which are separated by ",".
             Each tag must have between 2-20 characters.'''
                messages.error(request, {'title': 'ERROR:', 'message_content': tags_error_msg})
        else:
            messages.error(request, {'title': 'ERROR:',
                           'message_content': 'Invalid data. Book number must be between 1-999.'})
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


def user_page(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    users_questions = Question.get_all_user_questions(profile)
    users_answers = Answer.get_all_user_answers(profile)
    context = {
        'profile': profile,
        'user_questions': users_questions,
        'user_answers': users_answers,
    }
    return render(request, 'home/user_page.html', context)


class DeleteQuestionView(DeleteView):
    model = Question

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.profile == request.profile:
            messages.success(request, 'SUCCESS: Your question has been deleted.')
            return super(DeleteQuestionView, self).delete(request, *args, **kwargs)
        else:
            return HttpResponse('Unauthorized', status=401)

    def get_success_url(self):
        return reverse_lazy('explore-page')
