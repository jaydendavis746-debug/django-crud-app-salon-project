
from django.shortcuts import render
from django.http import HttpResponse

from .models import Service, StylistService, Availability
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView


def home(request):

    return HttpResponse('<h1>Welcome to this salon </h1>')


def about(request):
    return render(request, 'about.html')

class ServiceList(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'


class ServiceDetail(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['stylist_services'] = (
            StylistService.objects.filter(service=self.object, stylist__is_superuser=True).select_related('stylist')
        )

        return context


class StylistDetail(DetailView):
    model = User
    template_name = 'stylists/stylist_detail.html'
    context_object_name= 'stylist'

    def get_queryset(self):
        return User.objects.filter(is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stylist_services'] = (
            StylistService.objects.filter(stylist=self.object).select_related('service')
        )    

        context['availabilities'] = (
            Availability.objects.filter(stylist=self.object, is_booked=False).order_by('date', 'time')
        )

        return context