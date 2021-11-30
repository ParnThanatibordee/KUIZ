import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from KUIZ.models import Quiz


def create_question(quiz_topic, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Quiz.objects.create(quiz_topic=quiz_topic, pub_date=time)


class QuizIndexViewTests(TestCase):
    def test_no_quiz(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('KUIZ:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No quiz are available.")
        self.assertQuerysetEqual(response.context['latest_quiz_list'], [])

    def test_past_quiz(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        quiz = create_question(quiz_topic="Past quiz.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_quiz_list'],
            [quiz],
        )

    def test_future_quiz(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(quiz_topic="Future quiz.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No quiz are available.")
        self.assertQuerysetEqual(response.context['latest_quiz_list'], [])

    def test_future_quiz_and_past_quiz(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        quiz = create_question(quiz_topic="Past quiz.", days=-30)
        create_question(quiz_topic="Future quiz.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_quiz_list'],
            [quiz],
        )

    def test_two_past_quiz(self):
        """
        The questions index page may display multiple questions.
        """
        quiz1 = create_question(quiz_topic="Past quiz 1.", days=-30)
        quiz2 = create_question(quiz_topic="Past quiz 2.", days=-5)
        response = self.client.get(reverse('KUIZ:index'))
        self.assertQuerysetEqual(
            response.context['latest_quiz_list'],
            [quiz2, quiz1],)
        
class QuestionDetailViewTests(TestCase):
    """A class for checking detail view."""

    def setUp(self):
        self.user = User.objects.create_user(username='username', email='testemail@mail.com', password='147896325')
        # self.user.first_name = "testuser"
        # self.user.last_name = "hello"
        # self.user.save()

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns to index page."""
        self.client.login(username='username', password='qwerxhucj12')
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        self.client.login(username='username', password='qwerxhucj12')
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
