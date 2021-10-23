from django.shortcuts import render
from django.http import HttpResponse

from KUIZ.models import Quiz


def index(request):
    """Index homepage."""
    all_quiz = Quiz.objects.all()
    output = '\n'.join([q.quiz_topic for q in all_quiz])
    return HttpResponse(output)


def exam(request):
    """Exam view."""
    pass


def question(request):
    """Question view."""
    pass


def answer(request):
    """Answer for choice or type."""
    pass


def result(request):
    """Result of the exam page."""
    pass


def feedback(request):
    """Feedback page for discuss with teacher."""
    pass
