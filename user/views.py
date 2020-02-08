from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, reverse, redirect
from django.views.generic import FormView, TemplateView
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


class SiteLogoutView(LogoutView):
    def get_next_page(self):
        return reverse('marketplace:main')


class ProfileChose(TemplateView):
    template_name = 'accounts/profile.html'


class TuroperatorProfileView(TemplateView):
    template_name = 'accounts/profile_turoperator.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass