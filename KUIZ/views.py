from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
import datetime
import random

from .forms import FeedbackForm, NewQuizForm, NewQuestionForm, NewMultipleChoiceForm, NewTypingChoiceForm
from account.models import Account
from KUIZ.models import Quiz, Feedback, Question, Attendee, Choice, Type, Answer, Score, ClassroomUser
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

start_time = None


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


@login_required(login_url='login')
def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = list(quiz.question_set.all())
    user_contain = [i.user for i in list(ClassroomUser.objects.filter(quiz=quiz))]
    remaining_message = ""
    error_message = ""
    global start_time
    start_time = None

    if quiz.private and (request.user not in user_contain) and (request.user != quiz.owner):
        return render(request, 'KUIZ/password.html',
                      {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                       'time': quiz.exam_duration,
                       'remain_message': remaining_message,
                       'error_message': error_message})

    if quiz.can_vote():
        user_attendee = Attendee.objects.filter(user=request.user, quiz=quiz)
        if quiz.limit_attempt_or_not and (request.user != quiz.owner):
            remaining_message = f" (remaining attempt: {quiz.attempt - len(user_attendee)})"
            if len(user_attendee) >= quiz.attempt:
                return render(request, 'KUIZ/out_of_attempt.html',
                              {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                               'time': quiz.exam_duration,
                               'remain_message': remaining_message})
        all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz)
        if len(all_answer_in_quiz) > 0:
            for i in all_answer_in_quiz:
                i.delete()
        try:
            question1_id = all_question[0].pk
        except:
            return render(request, 'KUIZ/no_question.html',
                          {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                           'time': quiz.exam_duration,
                           'remain_message': remaining_message})
        return render(request, 'KUIZ/exam.html',
                      {'quiz': quiz, 'q1_id': question1_id, 'num_of_question': len(list(quiz.question_set.all())),
                       'time': quiz.exam_duration,
                       'remain_message': remaining_message})
    else:
        return render(request, 'KUIZ/cannot_vote.html',
                      {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                       'time': quiz.exam_duration,
                       'remain_message': remaining_message})


@login_required(login_url='login')
def password(request, pk):
    """Password view"""
    quiz = Quiz.objects.get(pk=pk)

    try:
        input_password = request.POST['password']
    except:
        input_password = ""
    remaining_message = ""
    if input_password == "":
        error_message = "* please enter your password!"
        return render(request, 'KUIZ/password.html',
                      {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                       'time': quiz.exam_duration,
                       'remain_message': remaining_message,
                       'error_message': error_message})
    else:
        if input_password == quiz.password:
            ClassroomUser.objects.create(quiz=quiz, user=request.user)
            return HttpResponseRedirect(reverse('exam', args=(pk,)))
        else:
            error_message = "* wrong password!"
            return render(request, 'KUIZ/password.html',
                          {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                           'time': quiz.exam_duration,
                           'remain_message': remaining_message,
                           'error_message': error_message})


@login_required(login_url='login')
def clear_answer(request, pk, question_id):
    """Clear answer view"""
    question = Question.objects.get(pk=question_id)
    all_answer_in_question = Answer.objects.filter(user=request.user, question=question)
    if len(all_answer_in_question) > 0:
        for i in all_answer_in_question:
            i.delete()
    return HttpResponseRedirect(reverse('question', args=(pk, question_id)))


@login_required(login_url='login')
def question(request, pk, question_id):
    """Question view."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = list(quiz.question_set.all())
    if quiz.can_vote():
        try:
            num_of_question = all_question.index(
                Question.objects.get(pk=question_id))
        except:
            return HttpResponseRedirect(reverse('exam', args=(pk,)))
        this_question = all_question[num_of_question]
        type_or_not = False
        all_choice = this_question.choice_set.all()
        if len(all_choice) == 0:
            all_choice = this_question.type_set.all()
            if len(all_choice) > 1:
                all_choice = all_choice[0]
            type_or_not = True
        else:
            choices = {}
            for i in range(len(all_choice)):
                choices[chr(i + 65)] = all_choice[i]
        back_question = ""
        next_question = ""
        back_link = False
        if num_of_question > 0:
            back_question = all_question[num_of_question - 1]
            back_link = True
        if not back_link:
            global start_time
            if start_time == None:
                start_time = datetime.datetime.now()
        try:
            next_question = all_question[num_of_question + 1]
            next_link = True
        except:
            next_link = False
        answer_in_question = list(Answer.objects.filter(user=request.user, quiz=quiz, question=this_question))
        if len(answer_in_question) > 0:
            lastest_answer_in_question = answer_in_question[-1]
        else:
            lastest_answer_in_question = None
        now = datetime.datetime.now()
        current_time = (now - start_time).total_seconds()
        time_diff = (quiz.exam_duration * 60) - current_time
        if (int(time_diff // 60)//10) == 0:
            if (int(time_diff % 60))//10 == 0:
                result_time = f"0{int(time_diff // 60)}:0{int(time_diff % 60)}"
            else:
                result_time = f"0{int(time_diff // 60)}:{int(time_diff % 60)}"
        else:
            if (int(time_diff % 60))//10 == 0:
                result_time = f"{int(time_diff // 60)}:0{int(time_diff % 60)}"
            else:
                result_time = f"{int(time_diff // 60)}:{int(time_diff % 60)}"
        if type_or_not:
            return render(request, 'KUIZ/type_question.html', {'quiz': quiz, 'question': this_question,
                                                               'num': num_of_question + 1,
                                                               'max_num': len(list(quiz.question_set.all())),
                                                               'choices': all_choice, 'next_link': next_link,
                                                               'next_question': next_question, 'back_link': back_link,
                                                               'back_question': back_question,
                                                               'time': quiz.exam_duration, 'remaining_time': result_time,
                                                               'lastest_answer_in_question': lastest_answer_in_question})
        else:
            return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question,
                                                          'num': num_of_question + 1,
                                                          'max_num': len(list(quiz.question_set.all())),
                                                          'choices': choices, 'next_link': next_link,
                                                          'next_question': next_question, 'back_link': back_link,
                                                          'back_question': back_question, 'time': quiz.exam_duration,
                                                          'remaining_time': result_time,
                                                          'lastest_answer_in_question': lastest_answer_in_question})
    else:
        return render(request, 'KUIZ/cannot_vote.html',
                      {'quiz': quiz, 'num_of_question': len(list(quiz.question_set.all())),
                       'time': quiz.exam_duration,
                       'remain_message': ""})


@login_required(login_url='login')
def answer(request, pk, question_id):
    """Answer for choice or type."""
    quiz = Quiz.objects.get(pk=pk)
    all_question = list(quiz.question_set.all())
    question = get_object_or_404(Question, pk=question_id)
    all_choice = question.choice_set.all()
    if len(all_choice) == 0:
        all_choice = question.type_set.all()
    try:
        if isinstance(all_choice[0], Choice):
            try:
                choice_id = request.POST['choice']
                selected_choice = question.choice_set.get(pk=choice_id)
            except (KeyError, Choice.DoesNotExist):
                all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz, question=question)
                if len(all_answer_in_quiz) > 0:
                    for i in all_answer_in_quiz:
                        i.delete()
                Answer.objects.create(user=request.user, quiz=quiz, question=question,
                                      answer="")
                try:
                    num_of_question = all_question.index(
                        Question.objects.get(pk=question_id))
                except:
                    return HttpResponseRedirect(reverse('exam', args=(pk,)))
                try:
                    next_question = all_question[num_of_question + 1].pk
                    next_link = True
                except:
                    next_link = False
                if next_link:
                    return HttpResponseRedirect(reverse('question', args=(pk, next_question)))
                else:
                    return HttpResponseRedirect(reverse('result', args=(pk,)))
            else:
                all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz, question=question)
                if len(all_answer_in_quiz) > 0:
                    for i in all_answer_in_quiz:
                        i.delete()
                Answer.objects.create(user=request.user, quiz=quiz, question=question,
                                      answer=selected_choice.choice_text)
                try:
                    num_of_question = all_question.index(
                        Question.objects.get(pk=question_id))
                except:
                    return HttpResponseRedirect(reverse('exam', args=(pk,)))
                try:
                    next_question = all_question[num_of_question + 1].pk
                    next_link = True
                except:
                    next_link = False
                if next_link:
                    return HttpResponseRedirect(reverse('question', args=(pk, next_question)))
                else:
                    return HttpResponseRedirect(reverse('result', args=(pk,)))
        elif isinstance(all_choice[0], Type):
            try:
                answer = request.POST['type']
            except:
                answer = ""
                all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz, question=question)
                if len(all_answer_in_quiz) > 0:
                    for i in all_answer_in_quiz:
                        i.delete()
                Answer.objects.create(user=request.user, quiz=quiz, question=question, answer=answer)
                try:
                    num_of_question = all_question.index(
                        Question.objects.get(pk=question_id))
                except:
                    return HttpResponseRedirect(reverse('exam', args=(pk,)))
                try:
                    next_question = all_question[num_of_question + 1].pk
                    next_link = True
                except:
                    next_link = False
                if next_link:
                    return HttpResponseRedirect(reverse('question', args=(pk, next_question)))
                else:
                    return HttpResponseRedirect(reverse('result', args=(pk,)))
            else:
                all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz, question=question)
                if len(all_answer_in_quiz) > 0:
                    for i in all_answer_in_quiz:
                        i.delete()
                Answer.objects.create(user=request.user, quiz=quiz, question=question, answer=answer)
                try:
                    num_of_question = all_question.index(
                        Question.objects.get(pk=question_id))
                except:
                    return HttpResponseRedirect(reverse('exam', args=(pk,)))
                try:
                    next_question = all_question[num_of_question + 1].pk
                    next_link = True
                except:
                    next_link = False
                if next_link:
                    return HttpResponseRedirect(reverse('question', args=(pk, next_question)))
                else:
                    return HttpResponseRedirect(reverse('result', args=(pk,)))
    except:
        Answer.objects.create(user=request.user, quiz=quiz, question=question, answer="")
        try:
            num_of_question = all_question.index(
                Question.objects.get(pk=question_id))
        except:
            return HttpResponseRedirect(reverse('exam', args=(pk,)))
        try:
            next_question = all_question[num_of_question + 1].pk
            next_link = True
        except:
            next_link = False
        if next_link:
            return HttpResponseRedirect(reverse('question', args=(pk, next_question)))
        else:
            return HttpResponseRedirect(reverse('result', args=(pk,)))


@login_required(login_url='login')
def result(request, pk):
    """Report of score of user."""
    # automate or hand-check
    user = request.user  # เก็บ quiz score ไว้เป็น dict {user:score}
    quiz = Quiz.objects.get(pk=pk)
    score = 0
    max_score = 0  # should in model
    all_answer_in_quiz = Answer.objects.filter(user=user, quiz=quiz)
    Attendee.objects.create(user=user, quiz=quiz)
    logger.info(f"User {request.user.username} ({request.user}) has finished quiz {quiz.quiz_topic}.")
    if quiz.automate:
        for answer in all_answer_in_quiz:
            if answer.check_answer(answer.question.correct):
                score += answer.question.point
        for question in list(quiz.question_set.all()):
            max_score += question.point
    Score.objects.create(user=user, quiz=quiz, score=score, max_score=max_score)
    return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': score, 'max': max_score,
                                                'automate': quiz.automate})


@login_required(login_url='login')
def get_feedback(request):
    quiz = Quiz.objects.filter(owner=request.user)
    feedback = Feedback.objects.all()
    return render(request, "KUIZ/feedback.html", {"all_quiz": quiz, "feedback": feedback, "user": request.user})


@login_required(login_url='login')
def send_feedback(request, pk):
    quiz_filter = Quiz.objects.get(pk=pk)
    quiz = Quiz.objects.filter(pk=pk)
    student_attendee = Attendee.objects.filter(quiz=quiz_filter)
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"User {request.user.username} ({request.user}) has sent feedback to their student")
            return redirect('index')
    else:
        form = FeedbackForm()
        form.fields['quiz'].queryset = quiz
        form.fields['user'].queryset = student_attendee
    return render(request, "KUIZ/send_feedback.html", {"form": form, "user": request.user})


@login_required(login_url='login')
def new_quiz(request):
    """Create a new quiz by teacher."""
    if request.method == "POST":
        quiz_form = NewQuizForm(request.POST)
        if quiz_form.is_valid():
            try:
                quiz = quiz_form.save()
            except:
                return redirect('detail')
            quiz.owner = request.user
            logger.info(f"User {request.user.username} ({request.user}) has created a new quiz ({quiz.quiz_topic}).")
            quiz.save()
            return redirect('detail')
    else:
        quiz_form = NewQuizForm()
    return render(request, "KUIZ/new_quiz.html", {"quiz_form": quiz_form})


@login_required(login_url='login')
def edit_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if quiz.owner == request.user:
        quiz_form = NewQuizForm(initial={
            'quiz_topic': quiz.quiz_topic,
            'private': quiz.private,
            'password': quiz.password,
            'detail': quiz.detail,
            'topic': quiz.topic,
            'pub_date': quiz.pub_date,
            'end_date': quiz.end_date,
            'exam_duration': quiz.exam_duration,
            'random_order': quiz.random_order,
            'limit_attempt_or_not': quiz.limit_attempt_or_not,
            'attempt': quiz.attempt,
        })
        if request.method == "POST":
            quiz_form = NewQuizForm(request.POST, instance=quiz)
            if quiz_form.is_valid():
                try:
                    quiz = quiz_form.save()
                except:
                    return redirect('detail')
                quiz.save()
                return redirect('detail')
    else:
        return redirect('detail')
    return render(request, 'KUIZ/edit_quiz.html', {'quiz': quiz, 'quiz_form': quiz_form})


@login_required(login_url='login')
def check(request):
    all_owner_quiz = Quiz.objects.filter(owner=request.user)
    return render(request, 'KUIZ/checking.html', {'owner_quiz': all_owner_quiz})


@login_required(login_url='login')
def check_quiz(request, pk):
    this_quiz = Quiz.objects.get(pk=pk)
    all_student_attendee = Attendee.objects.filter(quiz=this_quiz)
    unique_list_student = {}
    for i in all_student_attendee:
        this_user = i.user.username
        if not (this_user in unique_list_student):
            unique_list_student[this_user] = i.user.id
    return render(request, 'KUIZ/checking_per_quiz.html', {"this_quiz": this_quiz, "all_user": unique_list_student})


@login_required(login_url='login')
def check_student(request, pk, id):
    this_quiz = Quiz.objects.get(pk=pk)
    this_user = Account.objects.get(pk=id)
    all_question = this_quiz.question_set.all()
    last_n_answer = []
    for i in all_question:
        last_n_answer.append(list(Answer.objects.filter(user=this_user, question=i))[-1])
    return render(request, 'KUIZ/checking_per_student.html', {'this_quiz': this_quiz, 'this_user': this_user,
                                                              'all_question': all_question,
                                                              'last_n_answer': last_n_answer})


@login_required(login_url='login')
def update_answer(request, pk, id):
    this_quiz = Quiz.objects.get(pk=pk)
    this_user = Account.objects.get(pk=id)
    all_question = this_quiz.question_set.all()
    score = 0
    max_score = 0
    for i in all_question:
        try:
            answer = request.POST[f"{i.pk}"]
        except:
            pass
        else:
            score += i.point
    for question in all_question:
        max_score += question.point
    Score.objects.create(user=this_user, quiz=this_quiz, score=score, max_score=max_score)
    return HttpResponseRedirect(reverse('check_per_quiz', args=(pk,)))


@login_required(login_url='login')
def new_question(request):
    """Create a new question by teacher."""
    if request.method == "POST":
        question_form = NewQuestionForm(request.POST)
        if question_form.is_valid():
            try:
                question = question_form.save()
            except:
                return redirect('detail')
            question.save()
            return redirect('detail')
    else:
        question_form = NewQuestionForm()
    question_form.fields['quiz'].queryset = Quiz.objects.filter(owner=request.user)
    return render(request, "KUIZ/new_question.html", {"question_form": question_form})


@login_required(login_url='/')
def select_question(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = quiz.question_set.all()
    return render(request, "KUIZ/select_question.html", {"questions": questions})


@login_required(login_url='login')
def edit_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    question_form = NewQuestionForm(initial={
        'quiz': question.quiz,
        'question_text': question.question_text,
        'correct': question.correct,
        'point': question.point
    })
    if request.method == "POST":
        question_form = NewQuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            try:
                question = question_form.save()
            except:
                return redirect('detail')
            question.save()
            return redirect('detail')
    return render(request, "KUIZ/edit_question.html", {"question": question, 'question_form': question_form})


@login_required(login_url='login')
def new_multiple_choice(request):
    """Create a new multiple choice by teacher."""
    if request.method == "POST":
        choice_form = NewMultipleChoiceForm(request.POST)
        if choice_form.is_valid():
            try:
                choice = choice_form.save()
            except:
                return redirect('detail')
            choice.save()
            return redirect('detail')
    else:
        choice_form = NewMultipleChoiceForm()
    quizzes = Quiz.objects.filter(owner=request.user)
    pk_list = [obj.pk for obj in quizzes]
    quizzes = Quiz.objects.filter(pk__in=pk_list)
    pk_question_list = []
    for pk in pk_list:
        for question in Quiz.objects.get(pk=pk).question_set.all():
            pk_question_list.append(question.pk)
    questions = Question.objects.filter(pk__in=pk_question_list)
    choice_form.fields['question'].queryset = questions
    return render(request, "KUIZ/new_multiple_choice.html", {"choice_form": choice_form})


@login_required(login_url='login')
def new_typing_choice(request):
    """Create a new typing choice by teacher."""
    if request.method == "POST":
        choice_form = NewTypingChoiceForm(request.POST)
        if choice_form.is_valid():
            try:
                choice = choice_form.save()
            except:
                return redirect('detail')
            choice.save()
            return redirect('detail')
    else:
        choice_form = NewTypingChoiceForm()
        quizzes = Quiz.objects.filter(owner=request.user)
    pk_list = [obj.pk for obj in quizzes]
    quizzes = Quiz.objects.filter(pk__in=pk_list)
    pk_question_list = []
    for pk in pk_list:
        for question in Quiz.objects.get(pk=pk).question_set.all():
            pk_question_list.append(question.pk)
    questions = Question.objects.filter(pk__in=pk_question_list)
    choice_form.fields['question'].queryset = questions
    return render(request, "KUIZ/new_typing_choice.html", {"choice_form": choice_form})


@login_required(login_url='login')
def select_question_to_edit_choice(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = quiz.question_set.all()
    return render(request, "KUIZ/select_question.html", {"questions": questions, 'choice': True})


@login_required(login_url='login')
def select_choice(request, question_id):
    question = Question.objects.get(pk=question_id)
    multiple_choices = question.choice_set.all()
    typing_choices = question.type_set.all()
    return render(request, "KUIZ/select_choice.html",
                  {'multiple_choices': multiple_choices, 'typing_choices': typing_choices})


@login_required(login_url='login')
def edit_multiple_choice(request, choice_id):
    choice = Choice.objects.get(pk=choice_id)
    choice_form = NewMultipleChoiceForm(initial={
        'question': choice.question,
        'choice_text': choice.choice_text
    })
    if request.method == "POST":
        choice_form = NewMultipleChoiceForm(request.POST, instance=choice)
        if choice_form.is_valid():
            try:
                choice = choice_form.save()
            except:
                return redirect('detail')
            choice.save()
            return redirect('detail')
    return render(request, "KUIZ/edit_multiple_choice.html", {"choice": choice, 'choice_form': choice_form})


@login_required(login_url='login')
def edit_typing_choice(request, choice_id):
    typing_choice = Type.objects.get(pk=choice_id)
    choice_form = NewTypingChoiceForm(initial={
        'question': typing_choice.question,
        'choice_text': typing_choice.choice_text,
    })
    if request.method == "POST":
        choice_form = NewTypingChoiceForm(request.POST, instance=typing_choice)
        if choice_form.is_valid():
            try:
                typing_choice = choice_form.save()
            except:
                return redirect('detail')
            typing_choice.save()
            return redirect('detail')
    return render(request, "KUIZ/edit_typing_choice.html", {"choice": typing_choice, 'choice_form': choice_form})


@login_required(login_url='login')
def member(request):
    all_owner_quiz = Quiz.objects.filter(owner=request.user)
    return render(request, 'KUIZ/member.html', {'owner_quiz': all_owner_quiz})


@login_required(login_url='login')
def member_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    classroom_user = ClassroomUser.objects.filter(quiz=quiz)
    return render(request, 'KUIZ/member_quiz.html', {'quiz': quiz, 'member': classroom_user})


@login_required(login_url='login')
def add_member_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    not_classroom_user = []
    classroom_user = [i.user.username for i in list(ClassroomUser.objects.filter(quiz=quiz))]
    all_user = list(Account.objects.all())
    for i in all_user:
        if not(i.username in classroom_user) and i.username != quiz.owner.username:
            not_classroom_user.append(i)
    return render(request, 'KUIZ/add_member_quiz.html', {'quiz': quiz, 'not_member': not_classroom_user})


@login_required(login_url='login')
def update_add_member_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    all_user = list(Account.objects.all())
    for i in all_user:
        try:
            add_user = request.POST[f"{i.id}"]
        except:
            pass
        else:
            ClassroomUser.objects.create(quiz=quiz, user=i)
    return HttpResponseRedirect(reverse('member_per_quiz', args=(pk,)))


@login_required(login_url='login')
def remove_member_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    classroom_user = ClassroomUser.objects.filter(quiz=quiz)
    return render(request, 'KUIZ/remove_member_quiz.html', {'quiz': quiz, 'member': classroom_user})


@login_required(login_url='login')
def update_remove_member_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    classroom_user = ClassroomUser.objects.filter(quiz=quiz)
    for i in classroom_user:
        try:
            remove_user = request.POST[f"{i.user.id}"]
        except:
            pass
        else:
            i.delete()
    return HttpResponseRedirect(reverse('member_per_quiz', args=(pk, )))
