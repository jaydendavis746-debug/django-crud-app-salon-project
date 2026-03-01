from django.contrib import admin
from .models import Service, StylistService, Availability, Appointment

admin.site.register(Service)
admin.site.register(StylistService)
admin.site.register(Availability)
admin.site.register(Appointment)
