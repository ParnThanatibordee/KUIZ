from .models import Feedback
from django.forms import ModelForm


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"