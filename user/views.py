from django.contrib.auth.views import LoginView
from django.shortcuts import render, reverse, redirect
from django.views.generic import FormView
from django.contrib.auth import login as auth_login

from .forms import LoginForm, RegisterForm
# Create your views here.


class SiteLoginView(LoginView):

    authentication_form = LoginForm

    def get_success_url(self):
        return reverse('marketplace:main')


class RegisterView(FormView):
    form_class = RegisterForm

    def get_success_url(self):
        return reverse('marketplace:main')

    def form_valid(self, form):
        auth_login(self.request, form.save())
        return super().form_valid(form)
