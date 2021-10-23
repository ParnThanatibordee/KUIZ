from django.shortcuts import render
from django.http import HttpResponse

from KUIZ.models import Quiz, Question


def index(request):
    """Index homepage."""
    return render(request, 'KUIZ/index.html')


def detail(request):
    """List of exam view."""
    all_question = Question.objects.all()
    return render(request, 'KUIZ/detail.html', {'questions': all_question})


def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'KUIZ/exam.html', {'quiz': quiz})


def question(request, pk, question_id):
    """Question view."""
    quiz = Quiz.objects.get(pk=pk)
    this_question = Question.objects.get(pk=question_id)
    num_of_question = 1
    return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question, 'num': num_of_question})


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
