from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name= models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    
    def __str__(self):
        return self.name


class StylistService(models.Model):
    stylist = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.stylist.username} - {self.service.name}'


class Availability(models.Model):
    stylist = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('stylist', 'date', 'time')

    
    def __str__(self):
        return f"{self.stylist.username} - {self.date} {self.time}"


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    stylist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.customer:
            return f'{self.customer.username} - {self.service.name}'
        return f'{self.guest_name} - {self.service.name}'