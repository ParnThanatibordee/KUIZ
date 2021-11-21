import datetime
from django.test import TestCase
from django.utils import timezone
from KUIZ.models import Quiz, Question


class QuizModelTests(TestCase):
    def test_quiz_form(self):
        quiz_name = Quiz(quiz_topic="Calculus I", detail="Derivative and Integration")
        self.assertEqual(quiz_name.__str__(), "Calculus I : Derivative and Integration")

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_quz = Quiz(pub_date=time)
        self.assertIs(future_quz.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_quiz = Quiz(pub_date=time)
        self.assertIs(old_quiz.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_quiz = Quiz(pub_date=time)
        self.assertIs(recent_quiz.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_quz = Quiz(pub_date=time)
        self.assertIs(future_quz.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        is_published() returns True for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_quiz = Quiz(pub_date=time)
        self.assertIs(old_quiz.is_published(), True)

    def test_is_published_with_recent_question(self):
        """
        is_published() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_quiz = Quiz(pub_date=time)
        self.assertIs(recent_quiz.is_published(), True)

    def test_can_vote_with_future_question(self):
        """
        can_vote() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_quz = Quiz(pub_date=time)
        self.assertIs(future_quz.can_vote(), False)

    def test_can_vote_with_old_question(self):
        """
        can_vote() returns True for questions whose pub_date and end_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_quiz = Quiz(pub_date=time, end_date=time + datetime.timedelta(days=1))
        self.assertIs(old_quiz.can_vote(), False)

    def test_can_vote_with_recent_question(self):
        """
        can_vote() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_quiz = Quiz(pub_date=time)
        self.assertIs(recent_quiz.can_vote(), True)


class QuestionModelTests(TestCase):
    def test_question_form(self):
        question_des = Question(question_text="What is derivative of x^3 + 2x - 5")
        self.assertEqual(question_des.__str__(), "What is derivative of x^3 + 2x - 5")
