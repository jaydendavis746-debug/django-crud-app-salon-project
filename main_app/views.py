
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse

from .models import Service, StylistService, Availability, Appointment
from .forms import AppointmentForm
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

# from django.contrib.auth.mixins import LoginRequiredMixin


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

        stylist_services= (
            StylistService.objects.filter(stylist=self.object).select_related('service')
        )    

        availabilities = (
            Availability.objects.filter(stylist=self.object, is_booked=False).order_by('date', 'time')
        )

        service_slots = []

        for ss in stylist_services:
            service_slots.append({
                'service': ss.service,
                'price': ss.price,
                'slots': availabilities
            })  

        context['service_slots'] = service_slots

        return context

class AppointmentCreate(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'bookings/appointment_form.html'

    def dispatch(self, request,*args, **kwargs):
        self.availability = get_object_or_404(Availability, id=kwargs['availability_id'])
        self.service = get_object_or_404(Service, id=kwargs['service_id'])
        if self .availability.is_booked:
            return redirect('stylist-detail', pk=self.availability.stylist.id)

        return super().dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        form.instance.stylist = self.availability.stylist
        form.instance.service = self.service
        form.instance.availability = self.availability
        if self.request.user.is_authenticated:
            form.instance.customer = self.request.user

        self.availability.is_booked=True
        self.availability.save()
        return super().form_valid(form)

    def get_success_url(self,):
        return reverse('booking-confirmation', kwargs={'pk' : self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



        
class BookingConfirmationDetail(DetailView):
    model = Appointment
    template_name = 'bookings/booking_confirmation.html'
    context_object_name = 'appointment'