from django.contrib import admin
from .models import Company, Products, ProductInteriorImgs, ProductExteriorImgs

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'ceo', 'est_year', 'origin']
    search_fields = ['name', 'ceo', 'origin']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'company', 'color', 'seat_Capacity', 'fuel_type', 'cc', 'mileage']
    search_fields = ['product_name', 'company__name', 'color', 'fuel_type']
    list_filter = ['company', 'fuel_type', 'color']

admin.site.register(ProductInteriorImgs)
admin.site.register(ProductExteriorImgs)