from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
from .forms import FeedbackForm, NewQuizForm
from KUIZ.models import Quiz, Feedback, Question, Attendee, Choice, Type, Answer, Score
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

    if quiz.can_vote():
        # add shuffle ถ้าจะ random order คำถาม quiz.question_set.all()
        global all_question
        all_question = list(quiz.question_set.all())
        all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz)
        if len(all_answer_in_quiz) > 0:
            for i in all_answer_in_quiz:
                i.delete()
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
                                                                'choices': all_choice, 'next_link': next_link,
                                                                'next_question': next_question, 'back_link': back_link,
                                                                'back_question': back_question, 'time': quiz.exam_duration,
                                                                'lastest_answer_in_question': lastest_answer_in_question})
        else:
            return render(request, 'KUIZ/question.html', {'quiz': quiz, 'question': this_question,
                                                          'num': num_of_question + 1, 'max_num': len(all_question),
                                                          'choices': choices, 'next_link': next_link,
                                                          'next_question': next_question, 'back_link': back_link,
                                                          'back_question': back_question, 'time': quiz.exam_duration,
                                                          'lastest_answer_in_question': lastest_answer_in_question})
    else:
        error_message = "quiz is not allow to at this time."
        return HttpResponse(error_message)


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
                # next iteration for collect ERROR
                # return HttpResponse(f'ERROR {question_id}')
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
            else:
                all_answer_in_quiz = Answer.objects.filter(user=request.user, quiz=quiz, question=question)
                if len(all_answer_in_quiz) > 0:
                    for i in all_answer_in_quiz:
                        i.delete()
                Answer.objects.create(user=request.user, quiz=quiz, question=question, answer=selected_choice.choice_text)
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
        elif isinstance(all_choice[0], Type):
            try:
                answer = request.POST['type']
            except:
                answer = ""
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
        else:
            return HttpResponse("ERROR")
    except:
        return HttpResponse("no choice")


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
        for question in all_question:
            max_score += question.point
        Score.objects.create(user=user, quiz=quiz, score=score, max_score=max_score)
        return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': score, 'max': max_score})
    else:
        #  will implement later
        # return render(request, 'KUIZ/result.html', {'quiz': quiz, 'score': score, 'max': max_score})
        return HttpResponse("Wait Teacher to check your quiz.")


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

