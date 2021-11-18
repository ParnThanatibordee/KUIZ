from django.db import models
from django.utils import timezone
from account.models import Account
import datetime
from django.conf import settings

TOPIC = [
    ('', '----------'),
    ('programming', 'Programming'),
    ('mathematics', 'Mathematics'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('biology', 'Biology'),
    ('astronomy', 'Astronomy'),
    ('social', 'Social'),
    ('sport', 'Sport'),
    ('others', 'Others'),
]

YES_OR_NO = [
    (True, 'Yes'),
    (False, 'No'),
]


class Quiz(models.Model):
    """Quiz model."""
    quiz_topic = models.CharField(max_length=200)
    # owner
    private = models.BooleanField(default=False)
    password = models.CharField(max_length=200, default="0000")
    detail = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date end', default=timezone.now() + datetime.timedelta(days=365))
    topic = models.CharField(max_length=20, choices=TOPIC, default='others')
    exam_duration = models.IntegerField(default=0)
    random_order = models.BooleanField(choices=YES_OR_NO, default=False)
    automate = models.BooleanField(choices=YES_OR_NO, default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            null=True,
                            blank=True,
                            on_delete=models.CASCADE)

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
    correct = models.CharField(max_length=200)
    point = models.IntegerField(default=1)

    def __str__(self):
        """Display question_text."""
        return self.question_text


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Display choice_text."""
        return self.choice_text


class Type(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, default="")

    def __str__(self):
        """Display choice_text."""
        return f"answer: {self.pk}"


class Score(models.Model):
    """Score model."""

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=-1)


class Answer(models.Model):
    """Answer model."""

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def check_answer(self, correct):
        if correct.lower() == str(self.answer).lower():
            return True
        return False

    def __str__(self):
        """Display answer"""
        return self.answer


class Feedback(models.Model):
    """Feedback model."""

    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=0)
    feedback_text = models.TextField(max_length=5000)

    def quiz_name(self):
        return self.quiz.quiz_topic

    def username(self):
        return self.user.username

    def __str__(self):
        """Display feedback_text"""
        return self.feedback_text


class Attendee(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
