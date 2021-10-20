from django.db import models


class Quiz(models.Model):
    """Quiz model."""

    quiz_topic = models.CharField(max_length=200)
    detail = models.CharField(max_length=200)
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
