from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_teacher')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login")


class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Please enter the new username'}))
    first_name = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Please enter the new first name'}))
    last_name = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Please enter the new last name'}))
    profile_pic = forms.ImageField(label=('Profile Picture'), required=False,
                                   error_messages={'invalid': ("Image files only")}, widget=forms.FileInput)
    is_teacher = forms.ChoiceField(choices=((True, 'Teacher'), (False, 'Student')), widget=forms.Select(),
                                   required=True)

    class Meta:
        model = Account
        fields = ('username', 'profile_pic', 'first_name', 'last_name', 'is_teacher')
