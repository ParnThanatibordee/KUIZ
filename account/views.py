from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from KUIZ.models import Attendee, Score, Quiz
from account.forms import RegistrationForm, AccountAuthenticationForm, ProfileForm

import logging

logger = logging.getLogger(__name__)


# Create your views here.
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            # account = authenticate(email=email, password=raw_password)
            login(request, user)
            logger.info(f"User {user.username} has registered({request.user})")
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logger.info(f"User {request.user.username} has logged out ({request.user})")
        logout(request)
    return redirect('index')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                logger.info(f"User {request.user.username} has logged in ({request.user})")
                return redirect('index')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context)


def profile_page(request):
    all_quiz = Quiz.objects.all()
    attendee = Attendee.objects.filter(user=request.user)
    attend_quiz = []
    for i in all_quiz:
        for j in attendee:
            if i.quiz_topic == j.quiz.quiz_topic:
                attend_quiz.append(i)
                break

    lastest_dict = {}
    for k in attend_quiz:
        try:
            lastest_score = list(Score.objects.filter(user=request.user, quiz=k))[-1]
            lastest_dict[k.quiz_topic] = lastest_score
        except:
            pass

    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'account/profile.html', {'score': lastest_dict, 'length_score': len(lastest_dict)})


def profile_edit_view(request):
    context = {}
    profile_form = ProfileForm(initial={
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    })
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info(f"User {request.user.username} has edited their profile ({request.user})")
            return redirect("profile")
    context['profile_form'] = profile_form
    return render(request, 'account/profile_edit.html', {'profile_form': profile_form, 'user': request.user})
