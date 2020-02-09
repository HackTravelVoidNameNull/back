from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from user.views import (HasGuidPermission,
                        HasParentPermission,
                        HasStudentPermission,
                        HasTeacherPermission,
                        HasTuroperatorPermission)
# Create your views here.


class MainView(TemplateView):
    template_name = 'main/main.html'

class TuroperatorConstructor(HasTuroperatorPermission, FormView):

