from django.utils.deprecation import MiddlewareMixin
from .forms import *


class RegisterLoginForm(MiddlewareMixin):

    def process_request(self, request):

        if request.method == 'GET' and not request.user.is_authenticated:

            request.register_form = RegisterForm()
            request.login_form = LoginForm()

        return None