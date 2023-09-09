from django.urls import path
from .views import RegistrationSuccessView, RegisterView, CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/success/', RegistrationSuccessView.as_view(), name='registration_success'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html', next_page="comments_list"), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
