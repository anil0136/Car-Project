from django.urls import path
from carsapp import views

urlpatterns = [  
    path('companylist/', views.company_list, name="company_list"),
    path('productslist/', views.product_list, name="product_list"),
    path('company/<int:company_id>/products/', views.company_products, name="company_products"),
    path('emi/', views.emi, name="emi"),
    path('details1/<int:product_id>/', views.details1, name="details1"),
]