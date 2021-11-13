from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FeedbackForm
from KUIZ.models import Quiz, Feedback, Question
from django.contrib.auth.decorators import login_required


def index(request):
    """Index homepage."""
    return render(request, 'KUIZ/index.html')


def home(request):
    return render(request, "KUIZ/home.html")


def detail(request):
    """List of exam view."""
    all_quiz = Quiz.objects.all()
    return render(request, 'KUIZ/detail.html', {'quizzes': all_quiz})


def detail_by_topic(request, topic):
    quiz_in_topic = Quiz.objects.filter(topic=topic)
    return render(request, 'KUIZ/detail_by_topic.html', {'quiz_in_topic': quiz_in_topic, 'topic': topic.title()})


@login_required(login_url='/login/')
def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    # add shuffle ถ้าจะ random order คำถาม quiz.question_set.all()
    all_question = quiz.question_set.all()
    question1 = all_question[0]
    return render(request, 'KUIZ/exam.html',
                  {'quiz': quiz, 'q1': question1, 'num_of_question': len(all_question), 'time': quiz.exam_duration})


@login_required(login_url='login')
def question(request, pk, question_id):
    """Question view."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = list(quiz.question_set.all())
    num_of_question = all_question.index(Question.objects.get(pk=question_id))
    this_question = all_question[num_of_question]
    all_choice = this_question.choice_set.all()
    text = 'Next'
    back_link = None
    if num_of_question > 0:
        back_question = all_question[num_of_question - 1]
        back_link = back_question.id
    # link = "{%url 'question' quiz.id next_question.id%}"
    try:
        next_question = all_question[num_of_question + 1]
        link = next_question.id
    except:
        next_question = this_question  # กัน error
        text = 'Submit'
        link = 'result'
    return render(request, 'KUIZ/question.html',
                  {'quiz': quiz, 'question': this_question, 'next_question': next_question, 'num': num_of_question + 1,
                   'choices': all_choice, 'text': text, 'link': link, 'back_link': back_link,
                   'max_num': len(all_question), 'time': quiz.exam_duration})


def answer(request, pk, question_id):
    """Answer for choice or type."""
    pass


@login_required(login_url='/login/')
def result(request, pk):
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
        return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': quiz.score, 'max': max_score})
    else:
        #  will implement later
        return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': quiz.score, 'max': max_score})


@login_required(login_url='/login/')
def get_feedback(request):
    feedback = Feedback.objects.all()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, "KUIZ/feedback.html", {"form": form, "feedback": feedback, "user": request.user})
