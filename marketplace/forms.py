from django import forms
from .models import *
from place.models import *


class MainTourInfo(forms.Form):

    global_tour = forms.ModelChoiceField(Route.objects.all())
    dormitory = forms.CharField(max_length=64)


class SingleRoute(forms.Form):

    place_start = forms.CharField()
    place_finish = forms.CharField()
    time_start = forms.TimeField()
    time_finish = forms.TimeField()
    queue = forms.IntegerField()

class ParentBranchChoose(forms.Form):

