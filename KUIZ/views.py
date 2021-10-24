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


def detail_by_section(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = quiz.question_set.all()
    return HttpResponse(questions)


def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = quiz.question_set.all()
    # add suffle ถ้าจะ random order คำถาม
    question1 = all_question[0]
    return render(request, 'KUIZ/exam.html', {'quiz': quiz, 'q1': question1})


def question(request, pk, question_id):
    """Question view."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = quiz.question_set.all()
    num_of_question = 1  # ต้องหาทาง update
    this_question = Question.objects.get(pk=question_id)
    next_question = Question.objects.get(pk=question_id+1)
    all_choice = this_question.choice_set.all()
    return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question, 'next_question': next_question, 'num': num_of_question, 'choices': all_choice})
    # ค่อยเพิ่ม if ใน question.html


def answer(request, pk, question_id):
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
