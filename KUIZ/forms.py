from .models import Feedback, Quiz
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

    class Meta:
        model = Quiz
        fields = ['quiz_topic', 'detail', 'topic', 'exam_duration', 'score']
        widgets = {
            'quiz_topic': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'exam_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
        }
