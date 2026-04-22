from django import urls
from rentalapp import views
from django.urls import path


urlpatterns = [
    path('rent', views.rent, name='rent'),
    path('details/<int:car_id>/', views.details, name='details'),
    path('check/<int:car_id>/', views.check, name='check'),
    path('frent<int:car_id>/', views.frent, name='frent'),
]


