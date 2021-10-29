from django.db import models
from django.utils import timezone
from account.models import Account
import datetime


class Quiz(models.Model):
    """Quiz model."""

    quiz_topic = models.CharField(max_length=200)
    detail = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date end', default=timezone.now() + datetime.timedelta(days=1))
    exam_duration = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        """Display quiz_topic and detail."""
        return f"{self.quiz_topic} : {self.detail}"


class Question(models.Model):
    """Question model."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    point = models.IntegerField(default=1)

    def __str__(self):
        """Display question_text."""
        return self.question_text


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        """Display choice_text."""
        return self.choice_text


class Feedback(models.Model):
    """Feedback model."""
    feedback_text = models.TextField(max_length=5000)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=0)

    def quiz_name(self):
        return self.quiz.quiz_topic

    def username(self):
        return self.user.username

    def __str__(self):
        """Display feedback_text"""
        return self.feedback_text
