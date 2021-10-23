import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Quiz, Question, Choice


class QuizModelTests(TestCase):
    def quiz_form(self):
        quiz_name = Quiz(quiz_topic="Calculus I", detail="Derivative and Integration")
        self.assertEqual(quiz_name.__str__(), "Calculus I : Derivative and Integration")


class QuestionModelTests(TestCase):
    def question_form(self):
        question_des = Question(question_text="What is derivative of x^3 + 2x - 5")
        self.assertEqual(question_des.__str__(), "What is derivative of x^3 + 2x - 5")
