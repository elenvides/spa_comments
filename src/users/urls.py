from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(), name='login-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
]
