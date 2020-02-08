from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, reverse, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from user.models import *
from turoperator.models import Turoperator
from .forms import *
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


class ProfileChose(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    # info about user from request

    def post(self, request, *args, **kwargs):
        chose = request.POST['chose'][0]
        if chose == 'teacher':
            request.user.role = SystemRole.objects.get_or_create(name='teacher')
            TeacherUser.objects.create(user=request.user)
        elif chose == 'student':
            request.user.role = SystemRole.objects.get_or_create(name='student')
            StudentUser.objects.create(user=request.user)
        elif chose == 'turoperator':
            request.user.role = SystemRole.objects.get_or_create(name='turoperator')
            Turoperator.objects.create(user=request.user)
        elif chose == 'parent':
            request.user.role = SystemRole.objects.get_or_create(name='parent')
            ParentUser.objects.create(user=request.user)
        elif chose == 'guid':
            request.user.role = SystemRole.objects.get_or_create(name='guid')
            Guid.objects.create(user=request.user)
        else:
            pass
        request.user.save()


class HasTeacherPermission(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin


class HasParentPermission(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_parent or self.request.user.is_admin

class HasTuroperatorPermission(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_turoperator or self.request.user.is_admin

class HasStudentPermission(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_student or self.request.user.is_admin


class TuroperatorProfileView(HasParentPermission, FormView):
    template_name = 'accounts/profile_turoperator.html'

    form_class = TuroperatorForm

    def form_valid(self, form):
        ret = super().form_valid(form)
        user = self.request.user
        turoperator = Turoperator.objects.get(user)
        turoperator.name = form.cleaned_data['name']
        turoperator.contact_data = form.contact_data['contact_data']
        return ret

    # user from reuest!!!!!!!!!!!!!!

    
