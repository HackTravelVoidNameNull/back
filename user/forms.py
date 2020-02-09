from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from .models import *
from school.models import School


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control',
                                          'placeholder': 'Пароль'}),
    )

    class Meta:
        model = SiteUser


class RegisterForm(UserCreationForm):

    error_messages = {
        'password_mismatch': 'пароли не совпадают',
    }

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )

    class Meta:
        model = SiteUser
        fields = ['email', 'phone_number', 'password1', 'password2']


class TuroperatorForm(forms.Form):

    name = forms.CharField(max_length=32)
    contact_data = forms.CharField(max_length=156)


class TeacherForm(forms.ModelForm):

    school = forms.ChoiceField(choices=School.objects.all())
    name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32)


class StudentsFormSchool(forms.ModelForm):

    student = forms.ChoiceField()


class StudentForm(models.Model):

    name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32)
    school = forms.ChoiceField(choices=School.objects.all())