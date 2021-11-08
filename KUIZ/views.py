from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random

from KUIZ.models import Quiz, Question, Choice, Feedback
from .forms import FeedbackForm


def index(request):
    """Index homepage."""
    return render(request, 'KUIZ/index.html')


def home(request):
    return render(request, "KUIZ/home.html", {})


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
    if quiz.can_vote():
        quiz.score = 0  # for test the real web app should record per user
        quiz.save()  # for test
        # add shuffle ถ้าจะ random order คำถาม quiz.question_set.all()
        global all_question
        all_question = list(quiz.question_set.all())
        if quiz.random_order:
            random.shuffle(all_question)
        try:
            question1 = all_question[0]
        except:
            return HttpResponse("There no question here.")
        return render(request, 'KUIZ/exam.html', {'quiz': quiz, 'q1': question1, 'num_of_question': len(all_question),
                                                  'time': quiz.exam_duration})
    else:
        error_message = "quiz is not allow to at this time."
        return HttpResponse(error_message)


def question(request, pk, question_id):
    """Question view."""
    # เพิ่มปุ่ม clear choice กับ mark
    quiz = Quiz.objects.get(pk=pk)
    if quiz.can_vote():
        num_of_question = all_question.index(
            Question.objects.get(pk=question_id))
        this_question = all_question[num_of_question]
        all_choice = this_question.choice_set.all()
        choices = {}
        for i in range(len(all_choice)):
            choices[chr(i + 65)] = all_choice[i]
        back_question = ""
        next_question = ""
        back_link = False
        if num_of_question > 0:
            back_question = all_question[num_of_question - 1]
            back_link = True
        try:
            next_question = all_question[num_of_question + 1]
            next_link = True
        except:
            next_link = False
        return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question,
                                                      'num': num_of_question + 1, 'max_num': len(all_question),
                                                      'choices': choices, 'next_link': next_link,
                                                      'next_question': next_question, 'back_link': back_link,
                                                      'back_question': back_question, 'time': quiz.exam_duration})
    else:
        error_message = "quiz is not allow to at this time."
        return HttpResponse(error_message)


def answer(request, pk, question_id):
    """Answer for choice or type."""
    quiz = Quiz.objects.get(pk=pk)
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # next iteration for collect ERROR
        return HttpResponse(f'ERROR {question_id}')
    else:
        if quiz.automate:
            if selected_choice.correct:
                quiz.score += question.point
            quiz.save()
        num_of_question = all_question.index(
            Question.objects.get(pk=question_id))
        try:
            next_question = all_question[num_of_question + 1].id
            next_link = True
        except:
            next_link = False
        if next_link:
            return HttpResponseRedirect(reverse('question', args=(pk, next_question)))
        else:
            return HttpResponseRedirect(reverse('result', args=(pk,)))


def result(request, pk):
    """Report of score of user."""
    # automate or hand-check
    automate = True  # for test
    user = request.user  # เก็บ quiz score ไว้เป็น dict {user:score}
    quiz = Quiz.objects.get(pk=pk)
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
