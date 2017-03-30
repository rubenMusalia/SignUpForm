from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings
from django.contrib.auth import authenticate
from django import forms
from django.forms import DateField


class RegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "The two passwords provided did not match (typo?)."
    }

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password2

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    birth_date = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')



