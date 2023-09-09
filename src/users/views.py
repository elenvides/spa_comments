from django.contrib.auth.views import LoginView
from .forms import UserLoginForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegisterUserForm
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView


User = get_user_model()


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('registration_success')

    def form_valid(self, form):
        User.objects.create_user(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        return super().form_valid(form)


class RegistrationSuccessView(TemplateView):
    template_name = 'users/registration_success.html'


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

