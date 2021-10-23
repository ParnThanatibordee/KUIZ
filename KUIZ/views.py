from django.shortcuts import render
from django.http import HttpResponse

from KUIZ.models import Quiz


def index(request):
    """Index homepage."""
    return HttpResponse("Hello, world. You're at the KUIZ index.")


def detail(request):
    """List of exam view."""
    all_quiz = Quiz.objects.all()
    output = '\n'.join([q.quiz_topic for q in all_quiz])
    return HttpResponse(output)


def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'KUIZ/exam.html', {'quiz': quiz})


def question(request):
    """Question view."""
    pass


def answer(request):
    """Answer for choice or type."""
    pass


def score(request):
    """Report of score of user."""
    pass


def result(request):
    """Result of the exam page."""
    pass


def feedback(request):
    """Feedback page for discuss with teacher."""
    pass
