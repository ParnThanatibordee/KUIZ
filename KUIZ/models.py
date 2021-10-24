from django.db import models
from django.utils import timezone
import datetime


class Quiz(models.Model):
    """Quiz model."""

    quiz_topic = models.CharField(max_length=200)
    detail = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    end_date = models.DateTimeField('date end', default=timezone.now() + datetime.timedelta(days=1))
    exam_duration = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def was_published_recently(self):
        """Check that the question was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check that the question was already published."""
        now = timezone.now()
        if now >= self.pub_date:
            return True
        return False

    def can_vote(self):
        """Check that the question can vote."""
        now = timezone.now()
        return self.end_date >= now >= self.pub_date

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
