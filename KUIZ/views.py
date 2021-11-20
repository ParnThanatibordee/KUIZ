from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
from .forms import FeedbackForm, NewQuizForm
from account.models import Account
from KUIZ.models import Quiz, Feedback, Question, Attendee, Choice, Type, Answer, Score, ClassroomUser
from django.contrib.auth.decorators import login_required


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


@login_required(login_url='/login')
def exam(request, pk):
    """Exam view."""
    quiz = Quiz.objects.get(pk=pk)
    remaining_message = ""
    global all_question
    all_question = list(quiz.question_set.all())
    user_contain = list(ClassroomUser.objects.filter(quiz=quiz))

    if quiz.private and (request.user not in user_contain):
        pass
    # not in classroom
    # return enter password page
    # add user to classroom

    if quiz.can_vote():
        user_attendee = Attendee.objects.filter(user=request.user, quiz=quiz)
        if quiz.limit_attempt_or_not and (request.user != quiz.user):
            remaining_message = f" (remaining attempt: {quiz.attempt - len(user_attendee)})"
            if len(user_attendee) >= quiz.attempt:
                return render(request, 'KUIZ/out_of_attempt.html', {'quiz': quiz, 'num_of_question': len(all_question),
                                                                    'time': quiz.exam_duration,
                                                                    'remain_message': remaining_message})
        all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz)
        if len(all_answer_in_quiz) > 0:
            for i in all_answer_in_quiz:
                i.delete()
        if quiz.random_order:
            random.shuffle(all_question)
        try:
            question1 = all_question[0]
        except:
            return render(request, 'KUIZ/no_question.html', {'quiz': quiz, 'num_of_question': len(all_question),
                                                             'time': quiz.exam_duration,
                                                             'remain_message': remaining_message})
        return render(request, 'KUIZ/exam.html', {'quiz': quiz, 'q1': question1, 'num_of_question': len(all_question),
                                                  'time': quiz.exam_duration,
                                                  'remain_message': remaining_message})
    else:
        return render(request, 'KUIZ/cannot_vote.html', {'quiz': quiz, 'num_of_question': len(all_question),
                                                         'time': quiz.exam_duration,
                                                         'remain_message': remaining_message})


def password(request, pk):
    """Password view"""
    pass


def question(request, pk, question_id):
    """Question view."""
    # เพิ่มปุ่ม clear choice กับ mark
    quiz = Quiz.objects.get(pk=pk)

    if quiz.can_vote():
        try:
            num_of_question = all_question.index(
                Question.objects.get(pk=question_id))
        except:
            return HttpResponseRedirect(reverse('exam', args=(pk, )))
        this_question = all_question[num_of_question]
        type_or_not = False
        all_choice = this_question.choice_set.all()
        if len(all_choice) == 0:
            all_choice = this_question.type_set.all()
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
        if type_or_not:
            return render(request, 'KUIZ/type_question.html', {'quiz': quiz, 'question': this_question,
                                                               'num': num_of_question + 1, 'max_num': len(all_question),
                                                               'choices': all_choice[0], 'next_link': next_link,
                                                               'next_question': next_question, 'back_link': back_link,
                                                               'back_question': back_question,
                                                               'time': quiz.exam_duration,
                                                               'lastest_answer_in_question': lastest_answer_in_question})
        else:
            return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question,
                                                          'num': num_of_question + 1, 'max_num': len(all_question),
                                                          'choices': choices, 'next_link': next_link,
                                                          'next_question': next_question, 'back_link': back_link,
                                                          'back_question': back_question, 'time': quiz.exam_duration,
                                                          'lastest_answer_in_question': lastest_answer_in_question})
    else:
        return render(request, 'KUIZ/cannot_vote.html', {'quiz': quiz, 'num_of_question': len(all_question),
                                                         'time': quiz.exam_duration,
                                                         'remain_message': ""})


def answer(request, pk, question_id):
    """Answer for choice or type."""
    quiz = Quiz.objects.get(pk=pk)
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
                    return HttpResponseRedirect(reverse('exam', args=(pk, )))
                try:
                    next_question = all_question[num_of_question + 1].id
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
                    next_question = all_question[num_of_question + 1].id
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
            else:
                all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz, question=question)
                if len(all_answer_in_quiz) > 0:
                    for i in all_answer_in_quiz:
                        i.delete()
                Answer.objects.create(user=request.user, quiz=quiz, question=question, answer=answer)
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
    except:
        try:
            num_of_question = all_question.index(
                Question.objects.get(pk=question_id))
        except:
            return HttpResponseRedirect(reverse('exam', args=(pk,)))
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
    user = request.user  # เก็บ quiz score ไว้เป็น dict {user:score}
    quiz = Quiz.objects.get(pk=pk)
    score = 0
    max_score = 0  # should in model
    all_answer_in_quiz = Answer.objects.filter(user=user, quiz=quiz)
    Attendee.objects.create(user=user, quiz=quiz)
    if quiz.automate:
        for answer in all_answer_in_quiz:
            if answer.check_answer(answer.question.correct):
                score += answer.question.point
        for question in list(quiz.question_set.all()):
            max_score += question.point
    Score.objects.create(user=user, quiz=quiz, score=score, max_score=max_score)
    return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': score, 'max': max_score,
                                                'automate': quiz.automate})


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


@login_required(login_url='/login')
def new_quiz(request):
    """Create a new quiz by teacher."""
    if request.method == "POST":
        quiz_form = NewQuizForm(request.POST)
        if quiz_form.is_valid():
            quiz_title = quiz_form.cleaned_data['quiz_topic']
            try:
                quiz = quiz_form.save()
            except:
                return redirect('detail')
            quiz.user = request.user
            quiz.save()
            return redirect('detail')
    else:
        quiz_form = NewQuizForm()
    return render(request, "KUIZ/new_quiz.html", {"quiz_form": quiz_form})


@login_required(login_url='/login')
def edit_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if quiz.user == request.user:
        quiz_form = NewQuizForm(initial={
            'quiz_topic': quiz.quiz_topic,
            'detail': quiz.detail,
            'topic': quiz.topic,
            'exam_duration': quiz.exam_duration,
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


def check(request):
    all_owner_quiz = Quiz.objects.filter(user=request.user)
    return render(request, 'KUIZ/checking.html', {'owner_quiz': all_owner_quiz})


def check_quiz(request, pk):
    this_quiz = Quiz.objects.get(pk=pk)
    all_student_attendee = Attendee.objects.filter(quiz=this_quiz)
    unique_list_student = {}
    for i in all_student_attendee:
        this_user = i.user.username
        if not (this_user in unique_list_student):
            unique_list_student[this_user] = i.user.id
    return render(request, 'KUIZ/checking_per_quiz.html', {"this_quiz": this_quiz, "all_user": unique_list_student})


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
    return HttpResponseRedirect(reverse('check_per_quiz', args=(pk, )))
