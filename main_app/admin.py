from django.contrib import admin
from .models import Service, StylistService, Availability, Booking

admin.site.register(Service)
admin.site.register(StylistService)
admin.site.register(Availability)
admin.site.register(Booking)
