from django.urls import path
from . import views 

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('services/', views.ServiceList.as_view(), name='service-list'),
  path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service-detail'),
  path('stylist/<int:pk>/', views.StylistDetail.as_view(), name='stylist-detail'),
  path('book/<int:availability_id>/<int:service_id>/', views.AppointmentCreate.as_view(), name='book-appointment'),


]
