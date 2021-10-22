from django.shortcuts import render, redirect
from django.http import HttpResponse

from KUIZ.models import Quiz

def index(request):
    return HttpResponse("Hello, world. You're at the KUIZ index.")


def home(request):
    return render(request,"KUIZ/home.html",{})

def detail(request):
    all_quiz = Quiz.objects.all()
    output = '\n'.join([q.quiz_topic for q in all_quiz])
    return HttpResponse(output)

