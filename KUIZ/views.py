from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FeedbackForm
from KUIZ.models import Quiz, Feedback


def index(request):
    return HttpResponse("Hello, world. You're at the KUIZ index.")


def home(request):
    return render(request, "KUIZ/home.html")


def detail(request):
    all_quiz = Quiz.objects.all()
    output = '\n'.join([q.quiz_topic for q in all_quiz])
    return HttpResponse(output)


def get_feedback(request):
    feedback = Feedback.objects.all()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, "KUIZ/feedback.html", {"form": form, "feedback": feedback})

