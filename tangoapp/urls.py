from django import forms
from django import urls
from tangoapp import views
from django.urls import path
urlpatterns = [
    path('',views.register,name='register'),
    path("login",views.user_login,name='login'),
    path("home",views.home,name='home'),
    path("profile",views.profile,name='profile'),
    path("logout",views.user_logout,name='logout'),
    path("update",views.user_update,name='update'),
    path("reset/", views.reset, name='reset'),

]