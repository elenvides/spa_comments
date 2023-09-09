from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from captcha.fields import CaptchaField


User = get_user_model()


class RegisterUserForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    captcha = CaptchaField()
