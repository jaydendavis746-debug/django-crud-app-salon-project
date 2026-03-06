
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse

from .models import Service, StylistService, Availability, Booking
from .forms import BookingForm
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError

from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Min, Max

def invalid_page(request):
    return render(request, "invalid.html", status=400)


def get_times_for_date(request, stylist_id):
    date = request.GET.get('date')

    times = Availability.objects.filter(
        stylist_id = stylist_id,
        date = date
    ).order_by('time').values_list('id', 'time')

    return JsonResponse(list(times), safe=False)

class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')

class ServiceList(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return(Service.objects.annotate(
            min_price=Min('stylistservice__price'),
            max_price=  Max('stylistservice__price')
        ))


class ServiceDetail(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return(Service.objects.annotate(
            min_price=Min('stylistservice__price'),
            max_price=  Max('stylistservice__price')
        ))

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
        if not StylistService.objects.filter( stylist=self.availability.stylist, service=self.service ).exists():
            return invalid_page(request)

        return super().dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        form.instance.stylist = self.availability.stylist
        form.instance.service = self.service
        form.instance.availability = self.availability
        if self.request.user.is_authenticated:
            form.instance.customer = self.request.user

        if self.availability.date < timezone.now().date():
            form.add_error(None, 'You cannot book a past date.')
            return self.form_invalid(form)

        if not StylistService.objects.filter(stylist = self.availability.stylist, service = self.service).exists():
            form.add_error(None,'This stylist does not offer this service.')
            return self.form_invalid(form)


        if self.availability.is_booked:
            form.add_error(None, 'This slot has just been booked by someone else.')
            return self.form_invalid(form)

        if self.request.user.is_authenticated:
            start_dt = datetime.combine(self.availability.date, self.availability.time)
            end_dt = start_dt + timedelta(minutes = self.service.duration)

            overlap = Booking.objects.filter(
                customer = self.request.user, 
                availability__date=self.availability.date, 
                availability__time = self.availability.time
                ).exists()
            if overlap:
                form.add_error(None, 'You already have a booking at this time.')
                return self.form_invalid(form)

        self.availability.is_booked=True
        self.availability.save(update_fields=['is_booked'])
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()

        stylist_service = StylistService.objects.get(
            stylist = booking.stylist,
            service = booking.service
        )

        context['price'] = stylist_service.price
        return context



    def dispatch(self, request, *args, **kwargs): 
        booking = self.get_object()

        if not StylistService.objects.filter(
            stylist=booking.availability.stylist,
            service=booking.service
        ).exists():
            return invalid_page(request)

        return super().dispatch(request, *args, **kwargs)


    def test_func(self):
        booking = self.get_object()
        return booking.customer == self.request.user


class BookingUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Booking
    fields = [ 'availability']
    template_name = 'bookings/booking_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()

        context['available_dates']= (
            Availability.objects.filter(stylist=booking.stylist)
            .order_by('date')
            .values_list('date', flat=True)
            .distinct()
        )

        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        booking = self.get_object()

        form.fields['availability'].queryset= Availability.objects.filter(
            stylist = booking.stylist,
            date__gte=booking.created_at.date()
        ).order_by('date', 'time')

        return form


    def test_func(self):
        booking = self.get_object()
        return booking.customer == self.request.user

    def form_valid(self, form):
        old_availability = self.get_object().availability
        new_availability = form.cleaned_data['availability']
        booking = self.get_object()
        
        if new_availability.date < timezone.now().date():
            form.add_error(None, 'You cannot book a past date.')
            return self.form_invalid(form)

        if not StylistService.objects.filter(stylist = booking.availability.stylist, service = booking.service).exists():
            form.add_error(None,'This stylist does not offer this service.')
            return self.form_invalid(form)


        if new_availability.is_booked and new_availability != old_availability:
            form.add_error(None, 'This slot has already been booked.')
            return self.form_invalid(form)


            overlap = Booking.objects.filter(
                customer = self.request.user, 
                availability__date=new_availability.date, 
                availability__time = new_availability.time
                ).exclude(id=booking.id).exists()
            if overlap:
                form.add_error(None, 'You already have a booking at this time.')
                return self.form_invalid(form)

        if old_availability != new_availability:
            old_availability.is_booked = False
            old_availability.save(update_fields=['is_booked'])

            new_availability.is_booked = True
            new_availability.save(update_fields=['is_booked'])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('booking-detail', kwargs={'pk': self.object.pk})


class BookingDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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
        return booking.customer == self.request.user


    def post(self, request, *args, **kwargs):
        print("POST METHOD CALLED")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        self.availability.is_booked = False
        self.availability.save(update_fields=['is_booked'])
        print("DELETE METHOD CALLED")
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


#---------------------------------------------------------------------------------Stylists Views----------------------------------------------------------------------------------------------------------------------------

class StylistRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'stylistprofile'):
            return redirect('home')
        return super().dispacth(request, *args, **kwargs) 


class StylistTemplate(StylistRequiredMixin, TemplateView):
    template_name='stylists/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stylist_user = self.request.user
        stylist_profile = getattr(stylist_user, 'stylistprofile', None)

        upcoming = Booking.objects.filter(
            stylist = stylist_user,
            availability__date__gte=timezone.now().date()
        ).order_by('availability__date', 'availability__time')

        context['stylist'] = stylist_profile
        context['upcoming'] = upcoming
        return context


class AvailabilityList(StylistRequiredMixin, ListView):
    model = Availability
    template_name = "stylists/availability_list.html"
    context_object_name = "slots"

    def get_queryset(self):
        stylist_user = self.request.user
        return Availability.objects.filter(
            stylist=stylist_user
        ).order_by("date", "time")


class AvailabilityCreate(StylistRequiredMixin, CreateView):
    model = Availability
    fields = ["date", "time"]
    template_name = "stylists/availability_form.html"
    success_url = reverse_lazy("stylist-availability")

    def form_valid(self, form):
        form.instance.stylist = self.request.user
        return super().form_valid(form)


class AvailabilityUpdate(StylistRequiredMixin, UpdateView):
    model = Availability
    fields = ["date", "time"]
    template_name = "stylist/availability_form.html"
    success_url = reverse_lazy("stylist-availability")

    def get_queryset(self):
        return Availability.objects.filter(stylist=self.request.user)


class AvailabilityDelete(StylistRequiredMixin, DeleteView):
    model = Availability
    template_name = "stylists/availability_confirm_delete.html"
    success_url = reverse_lazy("stylist-availability")

    def get_queryset(self):
        return Availability.objects.filter(stylist=self.request.user)




class RoleBasedLogin(LoginView):
     template_name = "registration/login.html"

     def get_success_url(self):
        user = self.request.user
        if hasattr(user,'stylistprofile'):
            return reverse('stylist-dashboard')
        return reverse('home')