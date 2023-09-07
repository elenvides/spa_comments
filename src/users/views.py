from django.views import View
from .forms import RegisterUserForm
from django.http import JsonResponse, HttpRequest

import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model


User = get_user_model()


@method_decorator(require_POST, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"errors": {"non_field_errors": ["Invalid JSON data"]}}, status=400)

        form = RegisterUserForm(data)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            return JsonResponse({"message": "User registered successfully"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
