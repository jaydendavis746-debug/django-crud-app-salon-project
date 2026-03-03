
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse

from .models import Service, StylistService, Availability, Booking
from .forms import BookingForm
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class Home(LoginView):
    template_name = 'home.html'


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

class BookingCreate(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

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
    model = Booking
    template_name = 'bookings/booking_confirmation.html'
    context_object_name = 'booking'



class BookingsList(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return (Booking.objects.filter(customer=self.request.user).select_related('service', 'stylist', 'availability').order_by('availability__date','availability__time'))


class BookingDetail(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def test_func(self):
        booking = self.get_object()
        return booking.customer == self.request.user


class BookingUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Booking
    fields = [ 'availability']
    template_name = 'bookings/booking_update.html'

    def test_func(self):
        booking = self.get_object()
        return booking.customer == self.request.user

    def form_valid(self, form):
        old_availability = self.get_object().availability
        new_availability = form.cleaned_data['availability']

        if old_availability != new_availability:
            old_availability.is_booked = False
            old_availability.save()

            new_availability.is_booked = True
            new_availability.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('booking-detail', kwargs={'pk': self.object.pk})


class BookingDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    print("BookingDelete CLASS LOADED")
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    context_object_name = 'booking'
    success_url = reverse_lazy('booking-list')

    def dispatch(self, request, *args, **kwargs):
        self.booking = self.get_object()
        self.availability = self.booking.availability
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        booking = self.get_object()
        print("TEST FUNC:", booking.customer, self.request.user)
        return booking.customer == self.request.user


    def post(self, request, *args, **kwargs):
        print("POST METHOD CALLED")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print("DELETE METHOD CALLED")

        self.availability.is_booked = False
        self.availability.save(update_fields=['is_booked'])

        return super().delete(request, *args, **kwargs)





def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('service-list')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
