import datetime
from django.test import TestCase
from django.utils import timezone
from account.models import Account
from KUIZ.models import Quiz, ClassroomUser, Question, Choice, Type, Score, Answer, Feedback, Attendee


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


class ClassroomUserModelTests(TestCase):
    def test_classroom_user_form(self):
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="Basic Math")
        classroom_user = ClassroomUser(quiz=quiz, user=user)
        self.assertEqual(classroom_user.__str__(), "DemoTester in Basic Math")


class QuestionModelTests(TestCase):
    def test_question_form(self):
        question_des = Question(question_text="What is derivative of x^3 + 2x - 5")
        self.assertEqual(question_des.__str__(), "What is derivative of x^3 + 2x - 5")


class ChoiceModelTests(TestCase):
    def test_choice_form(self):
        question = Question(question_text="1+1=?")
        choice_text = "2"
        choice = Choice(question=question, choice_text=choice_text)
        self.assertEqual(choice.__str__(), choice_text)


class TypeUserModelTests(TestCase):
    def test_type_form(self):
        question = Question(question_text="1+1=?")
        choice_text = "Answer here:"
        choice = Type(question=question, choice_text=choice_text)
        self.assertEqual(choice.__str__(), f"answer: {choice.pk}")


class ScoreModelTests(TestCase):
    pass


class AnswerModelTests(TestCase):
    def test_type_form(self):
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="Basic Math")
        question = Question(question_text="1+1=?", check_strategy="static")
        answer = Answer(user=user, quiz=quiz, question=question, answer="2")
        self.assertEqual(answer.__str__(), "2")

    def test_check_answer_with_static_strategy(self):
        """
        check_answer(correct) with static strategy returns True
        for answer whose has the correct answer and return False
        for the incorrect answer.
        """
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="English vocabulary")
        correct_answer = "apple"
        my_answer1 = "apple"
        question = Question(question_text="type apple", check_strategy="static", correct=correct_answer)
        answer1 = Answer(user=user, quiz=quiz, question=question, answer=my_answer1)
        self.assertEqual(answer1.check_answer(question.correct), True)
        my_answer2 = "Apple"
        answer2 = Answer(user=user, quiz=quiz, question=question, answer=my_answer2)
        self.assertEqual(answer2.check_answer(question.correct), False)

    def test_check_answer_with_flexible_strategy(self):
        """
        check_answer(correct) with flexible strategy returns True
        for answer whose has the correct answer and return False
        for the incorrect answer.
        """
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="English vocabulary")
        correct_answer = "apple"
        my_answer1 = "apple"
        question = Question(question_text="type apple", check_strategy="flexible", correct=correct_answer)
        answer1 = Answer(user=user, quiz=quiz, question=question, answer=my_answer1)
        self.assertEqual(answer1.check_answer(question.correct), True)
        my_answer2 = "Apple"
        answer2 = Answer(user=user, quiz=quiz, question=question, answer=my_answer2)
        self.assertEqual(answer2.check_answer(question.correct), True)

    def test_check_answer_with_white_space_order_strategy(self):
        """
        check_answer(correct) with white_space_order strategy returns True
        for answer whose has the correct answer and return False
        for the incorrect answer.
        """
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="English vocabulary")
        correct_answer = "apple banana"
        my_answer1 = "apple       banana"
        question = Question(question_text="type 'apple banana'", check_strategy="white_space_order", correct=correct_answer)
        answer1 = Answer(user=user, quiz=quiz, question=question, answer=my_answer1)
        self.assertEqual(answer1.check_answer(question.correct), True)
        my_answer2 = "banana apple"
        answer2 = Answer(user=user, quiz=quiz, question=question, answer=my_answer2)
        self.assertEqual(answer2.check_answer(question.correct), False)

    def test_check_answer_with_white_space_no_order_strategy(self):
        """
        check_answer(correct) with white_space_no_order strategy returns True
        for answer whose has the correct answer and return False
        for the incorrect answer.
        """
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="English vocabulary")
        correct_answer = "apple banana"
        my_answer1 = "apple       banana"
        question = Question(question_text="type 'apple banana'", check_strategy="white_space_no_order", correct=correct_answer)
        answer1 = Answer(user=user, quiz=quiz, question=question, answer=my_answer1)
        self.assertEqual(answer1.check_answer(question.correct), True)
        my_answer2 = "banana       apple"
        answer2 = Answer(user=user, quiz=quiz, question=question, answer=my_answer2)
        self.assertEqual(answer2.check_answer(question.correct), True)

    def test_check_answer_with_comma_order_strategy(self):
        """
        check_answer(correct) with comma_order strategy returns True
        for answer whose has the correct answer and return False
        for the incorrect answer.
        """
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="English vocabulary")
        correct_answer = "apple, banana"
        my_answer1 = "apple, banana"
        question = Question(question_text="type 'apple banana'", check_strategy="comma_order", correct=correct_answer)
        answer1 = Answer(user=user, quiz=quiz, question=question, answer=my_answer1)
        self.assertEqual(answer1.check_answer(question.correct), True)
        my_answer2 = "banana, apple"
        answer2 = Answer(user=user, quiz=quiz, question=question, answer=my_answer2)
        self.assertEqual(answer2.check_answer(question.correct), False)

    def test_check_answer_with_comma_no_order_strategy(self):
        """
        check_answer(correct) with comma_no_order strategy returns True
        for answer whose has the correct answer and return False
        for the incorrect answer.
        """
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="English vocabulary")
        correct_answer = "apple, banana"
        my_answer1 = "apple, banana"
        question = Question(question_text="type 'apple banana'", check_strategy="comma_no_order", correct=correct_answer)
        answer1 = Answer(user=user, quiz=quiz, question=question, answer=my_answer1)
        self.assertEqual(answer1.check_answer(question.correct), True)
        my_answer2 = "banana, apple"
        answer2 = Answer(user=user, quiz=quiz, question=question, answer=my_answer2)
        self.assertEqual(answer2.check_answer(question.correct), True)


class FeedbackModelTests(TestCase):
    def test_classroom_user_form(self):
        user = Account(username="DemoTester")
        quiz = Quiz(quiz_topic="Basic Math")
        feedback_text = "Good job"
        feedback = Feedback(user=user, quiz=quiz, feedback_text=feedback_text)
        self.assertEqual(feedback.quiz_name(), "Basic Math")
        self.assertEqual(feedback.username(), "DemoTester")
        self.assertEqual(feedback.__str__(), "Good job")


class AttendeeModelTests(TestCase):
    pass
