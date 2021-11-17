from .models import Feedback, Quiz, Question, Choice, Type
from django.forms import ModelForm
from django import forms

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"


class NewQuizForm(ModelForm):
    exam_duration = forms.IntegerField(
        label='Exam duration (minutes):', 
        initial=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    private = forms.BooleanField(
        label='Private Quiz:',
        required=False,
        widget=forms.Select(choices=((True, 'Yes'), (False, 'No')), attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Password for Private Quiz:',
        initial='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'leave it blank if Public Quiz...'})
    )

    automate = forms.BooleanField(
        label='Automate Checking',
        required=False,
        widget=forms.Select(choices=((True, 'Yes'), (False, 'No')), attrs={'class': 'form-control'})
    )

    class Meta:
        model = Quiz
        fields = ['quiz_topic', 'detail', 'private', 'password', 'topic', 'exam_duration', 'random_order', 'automate']
        widgets = {
            'quiz_topic': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'random_order': forms.Select(attrs={'class': 'form-control'}),
        }

class NewQuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'correct', 'point']
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
            'correct': forms.TextInput(attrs={'class': 'form-control'}),
            'point': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class NewMultipleChoiceForm(ModelForm):

    class Meta:
        model = Choice
        fields = ['question', 'choice_text']
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
            'choice_text': forms.TextInput(attrs={'class': 'form-control'})
        }

class NewTypingChoiceForm(ModelForm):
    correct = forms.CharField(
        label='Correct Answer:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Type
        fields = ['question', 'correct']
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
        }
