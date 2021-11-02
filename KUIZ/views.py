from django.shortcuts import render
from django.http import HttpResponse

from KUIZ.models import Quiz, Question


def index(request):
    """Index homepage."""
    return render(request, 'KUIZ/index.html')


def detail(request):
    """List of exam view."""
    all_quiz = Quiz.objects.all()
    return render(request, 'KUIZ/detail.html', {'quizzes': all_quiz})


def detail_by_topic(request, topic):
    quiz_in_topic = Quiz.objects.filter(topic=topic)
    return render(request, 'KUIZ/detail_by_topic.html', {'quiz_in_topic': quiz_in_topic, 'topic': topic.title()})


def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    # add shuffle ถ้าจะ random order คำถาม quiz.question_set.all()
    all_question = quiz.question_set.all()
    question1 = all_question[0]
    return render(request, 'KUIZ/exam.html', {'quiz': quiz, 'q1': question1})


def question(request, pk, question_id):
    """Question view."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = list(quiz.question_set.all())
    num_of_question = all_question.index(Question.objects.get(pk=question_id))
    this_question = all_question[num_of_question]
    all_choice = this_question.choice_set.all()
    back_question = ""
    next_question = ""
    back_link = False
    if num_of_question > 0:
        back_question = all_question[num_of_question-1]
        back_link = True
    try:
        next_question = all_question[num_of_question+1]
        next_link = True
    except:
        next_link = False
    return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question,
                                                  'num': num_of_question + 1, 'choices': all_choice,
                                                  'next_link': next_link, 'next_question': next_question,
                                                  'back_link': back_link, 'back_question': back_question})


def answer(request, pk, question_id):
    """Answer for choice or type."""
    pass


def score(request, pk):
    """Report of score of user."""
    # automate or hand-check
    automate = True  # for test
    user = request.user
    quiz = Quiz.objects.get(pk=pk)
    all_question = list(quiz.question_set.all())
    max_score = 0  # should in model
    if automate:
        for question in all_question:
            # must add in user
            # if user.selected_choice.correct:
            #     quiz.score += question.point
            max_score += question.point
        return render(request, 'KUIZ/score.html', {'quiz': quiz, 'score': quiz.score, 'max': max_score})
    else:
        #  will implement later
        return render(request, 'KUIZ/score.html', {'quiz': quiz, 'score': quiz.score, 'max': max_score})


def result(request, pk):
    """Result of the exam page."""
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': quiz.score})


def feedback(request, pk):
    """Feedback page for discuss with teacher."""
    return HttpResponse("FEEDBACK")
