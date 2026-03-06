from django.urls import path
from . import views 

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('services/', views.ServiceList.as_view(), name='service-list'),
  path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service-detail'),
  path('stylist/<int:pk>/', views.StylistDetail.as_view(), name='stylist-detail'),
  path('book/<int:availability_id>/<int:service_id>/', views.BookingCreate.as_view(), name='book-appointment'),
  path('booking-confirmation/<int:pk>/', views.BookingConfirmationDetail.as_view(), name='booking-confirmation' ),
  path('bookings/', views.BookingsList.as_view(), name='booking-list'), 
  path('bookings/<int:pk>/', views.BookingDetail.as_view(), name='booking-detail'),
  path('bookings/<int:pk>/update/', views.BookingUpdate.as_view(), name='booking-update'),
  path('bookings/<int:pk>/delete/', views.BookingDelete.as_view(), name='booking-delete'),
  path('stylist/dashboard/', views.StylistTemplate.as_view(), name='stylist-dashboard'),
  path('stylist/profile/', views.StylistProfileView.as_view(), name='stylist-profile'),
  path("stylist/bookings/", views.StylistBookingList.as_view(), name="stylist-booking-list"),
  path("stylist/bookings/<int:pk>/delete/", views.StylistBookingDelete.as_view(), name="stylist-booking-delete"),
  path("stylist/availability/", views.AvailabilityList.as_view(), name="stylist-availability"),
  path("stylist/availability/add/", views.AvailabilityCreate.as_view(), name="availability-add"),
  path("stylist/availability/<int:pk>/edit/", views.AvailabilityUpdate.as_view(), name="availability-update"),
  path("stylist/availability/<int:pk>/delete/", views.AvailabilityDelete.as_view(), name="availability-delete"),
  path("stylist/services/", views.StylistServiceList.as_view(), name="stylist-services"),
  path("stylist/services/add/", views.StylistServiceCreate.as_view(), name="stylist-service-add"),
  path("stylist/services/<int:pk>/edit/", views.StylistServiceUpdate.as_view(), name="stylist-service-update"),
  path("stylist/services/<int:pk>/delete/", views.StylistServiceDelete.as_view(), name="stylist-service-delete"),


  path("api/times/<int:stylist_id>/", views.get_times_for_date, name="get_times_for_date"),
  path('accounts/signup/', views.signup, name='signup'),
  path("accounts/login/", views.RoleBasedLogin.as_view(), name="login"),
]
