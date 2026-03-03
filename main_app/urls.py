from django.urls import path
from . import views 

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('services/', views.ServiceList.as_view(), name='service-list'),
  path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service-detail'),
  path('stylist/<int:pk>/', views.StylistDetail.as_view(), name='stylist-detail'),
  path('book/<int:availability_id>/<int:service_id>/', views.AppointmentCreate.as_view(), name='book-appointment'),
  path('booking-confrimation/<int:pk>/', views.BookingConfirmationDetail.as_view(), name='booking-confirmation' ),
  path('bookings/', views.BookingsList.as_view(), name='booking-list'), 
  path('bookings/<int:pk>/', views.BookingDetail.as_view(), name='booking-detail'),

  path('accounts/signup/', views.signup, name='signup'),
]
