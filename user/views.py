from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, reverse, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from user.models import *
from turoperator.models import Turoperator, CommitForPhysicalTour
from .forms import *
from .forms import LoginForm, RegisterForm
from django.db.models import Q
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
        turoperator.save()
        return ret

    def get_context_data(self, **kwargs):
        turoperator = Turoperator.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['tours'] = CommitForPhysicalTour.objects.filter(tour__turoperator=turoperator)
        context['touroperator'] = turoperator
        context['curators'] = Guid.objects.filter(turoperator)
        return context

    # user from reuest!!!!!!!!!!!!!!


class TeacherProfileView(HasTeacherPermission, FormView):
    template_name = 'accounts/profile_teacher.html'

    form_class = TeacherForm

    def form_valid(self, form):
        ret = super().form_valid(form)
        user = self.request.user
        data = form.cleaned_data
        teacher = TeacherUser.objects.get(user=user)
        teacher.name = data['name']
        teacher.last_name = data['last_name']
        teacher.patronymic = data['patronymic']
        teacher.school = data['school']
        teacher.save()
        return ret


class TeacherProfileStudentsView(HasTeacherPermission, FormView):
    template_name = 'accounts/profile_teacher_studets.html'

    def get_form_class(self):
        teacher = TeacherUser.objects.get(self.request.user)

        class StudentsFormSchool(forms.ModelForm):

            student = forms.ChoiceField(choices=StudentUser.objects.filter(Q(school=teacher.school) and Q(teacheruser__contains=teacher)))

        return StudentsFormSchool

    def form_valid(self, form):
        ret = super().form_valid(form)
        user = self.request.user

        teacher = TeacherUser.objects.get(user=user)
        teacher.students.add(form.cleaned_data['student'])
        teacher.save()
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = TeacherUser.objects.get(self.request.user).students
        return context


class TeacherTourView(HasTeacherPermission, TemplateView):
    template_name = 'accounts/profile_teachers_tours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = TeacherUser.objects.get(user=self.request.user)
        context['tours'] = CommitForPhysicalTour.objects.filter(teacher=teacher)
        return context


class StudentProfileView(HasStudentPermission, FormView):
    template_name = 'accounts/profile_student.html'

    def form_valid(self, form):
        ret = super().form_valid(form)
        data = form.cleaned_data
        student = StudentUser.objects.get(user=self.request.user)
        student.name = data['name']
        student.last_name = data['last_name']
        student.patronymic = data['patronymic']
        student.school = data['school']
        student.save()
        return ret


class StudentTourView(HasStudentPermission, TemplateView):
    template_name = 'accounts/profile_student_tours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = StudentUser.objects.get(user=self.request.user)
        context['tours'] = CommitForPhysicalTour.objects.filter(student=student)
        return context


class ParentProfileView(HasParentPermission, TemplateView):
    template_name = 'accounts/profile_parent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = ParentUser.objects.get(user=self.request.user)
        context['children'] = StudentUser.objects.filter(parent=parent)
        return context

