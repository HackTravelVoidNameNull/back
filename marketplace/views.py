from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.views.generic import FormView, DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from marketplace.models import *
from turoperator.models import *
from place.models import *
from django.core.serializers import serialize
import json
import datetime

from user.views import (HasGuidPermission,
                        HasParentPermission,
                        HasStudentPermission,
                        HasTeacherPermission,
                        HasTuroperatorPermission)


# Create your views here.


class MainView(TemplateView):
    template_name = 'main/main.html'


class RouteDetail(TemplateView):

    def get_template_names(self):
        if self.kwargs['route_id'] == 1:
            return ['main/route_detail1.html']

        if self.kwargs['route_id'] == 2:
            return ['main/route_detail2.html']

        if self.kwargs['route_id'] == 3:
            return ['main/route_detail3.html']

        if self.kwargs['route_id'] == 4:
            return ['main/route_detail4.html']


def route_info(request, route_id):
    branches = Route.objects.get(id=route_id)
    response = {'branches': [branches[0].name, branches[1].name, branches[2].name, branches[3].name],
                'places': []}

    for place in Platform.objects.filter(branch__in=branches):
        response['places'].append({'name': place.name,
                                   'descriptiob': place.description,
                                   'place_ip': place.place.google_maps_place_id})

    return JsonResponse(response)


class TuroperatorConstructor(HasTuroperatorPermission, DetailView):
    template_name = 'constructors/turoperator_constructor.html'

    def post(self):
        json_data = json.loads(self.request.body)
        dormitory = json_data['dormitory_id']
        start_date = json_data['start_date']
        food_supply = json_data['food_supply']
        finish_date = json_data['finish_date']
        price = json_data['price']
        points = json_data['points']
        dormitory = Place.objects.get_or_create(google_maps_place_id=dormitory)
        turoperator = Turoperator.objects.get(user=self.request.user)
        phys = PhysicalTour.objects.create(dormitory=dormitory, food_supply=food_supply, turoperator=turoperator)
        phys.save()
        cpt = CommitForPhysicalTour.objects.create(price=price, date=start_date, finish_date=finish_date, tour=phys)
        cpt.save()
        for point in points:
            st = point['s_t']
            ft = point['f_t']
            platform_id = point['platform_id']
            queue = point['queue']
            platform = Platform.objects.get(id=platform_id)
            PhysicalTourRoute.objects.create(place=platform, time_start=st, time_finish=ft, tour=phys,
                                             queue_number=queue).save()

        return redirect(reverse('marketplace:main'))


class ParentNavigationView(HasParentPermission, TemplateView):
    template_name = 'constructors/parent_navigation.html'


class ParentRouteChoose(HasParentPermission, TemplateView):
    template_name = 'constructors/choose_route.html'


class TourFiltringMixin:

    def get_queryset(self):
        route_id = self.kwargs['route_id']
        return CommitForPhysicalTour.objects.filter(tour__route=Route.objects.get(id=route_id))

    def post(self):
        json_data = json.loads(self.request.body)
        food_supply = json_data['food_supply']
        date_stat = datetime.datetime.strptime(json_data['date_start'], '%d-%n-%Y')
        date_finish = datetime.datetime.strptime(json_data['date_finish'], '%d-%n-%Y')
        sorting = json_data['sorting']
        tours = self.get_queryset().filter(Q(date__gte=date_stat)
                                           and Q(finish_date__lte=date_finish)
                                           and Q(food_supply=food_supply))
        if sorting == '+':
            tours.oreder_by('price')
        else:
            tours.oreder_by('-price')

        return JsonResponse(serialize('json', tours))


class ParentTourChoose(HasParentPermission, TemplateView, TourFiltringMixin):
    template_name = 'constructors/choose_tour.html'


class TeacherTourChoose(HasTeacherPermission, TemplateView, TourFiltringMixin):
    template_name = 'constructors/choose_tour.html'
