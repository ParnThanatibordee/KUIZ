from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from KUIZ.models import Attendee
from account.forms import RegistrationForm, AccountAuthenticationForm, ProfileForm


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
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
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
                return redirect('index')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context)


def profile_page(request):
    attendee = Attendee.objects.filter(user = request.user)
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'account/profile.html', {'user': request.user, 'quiz_list': list(attendee)})


def profile_edit_view(request):
    context = {}
    profile_form = ProfileForm(request.POST, instance=request.user)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    context['profile_form'] = profile_form
    return render(request, 'account/profile_edit.html', {'profile_form': profile_form, 'user': request.user})
