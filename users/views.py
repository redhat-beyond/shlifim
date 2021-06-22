from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from home.models import Question, Answer
from .forms import SignUpForm
from django.contrib.auth import login, authenticate


def users(request):
    profiles = Profile.profiles_feed()
    return render(request, "users/users.html", {"profiles": profiles})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user.save()
            profile = Profile(user=user)
            user = authenticate(username=user.username, password=raw_password)
            profile.gender = form.cleaned_data.get("gender")
            profile.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def user_page(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    users_questions = Question.get_all_user_questions(profile)
    users_answers = Answer.get_all_user_answers(profile)
    context = {
        "profile": profile,
        "user_questions": users_questions,
        "user_answers": users_answers,
    }
    return render(request, "users/user_page.html", context)
