from django.db import models

# Create your models here.

from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    ceo = models.CharField(max_length=100)
    est_year = models.PositiveIntegerField()
    origin = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    seat_Capacity = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)
    cc = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    product_img = models.ImageField(upload_to='products', blank=True, null=True)
    price=models.PositiveIntegerField()
    

    def __str__(self):
        return self.product_name
    
class ProductInteriorImgs(models.Model):
    interior = models.ImageField(upload_to='interior', blank=True, null=True)
    product = models.ForeignKey(Products, related_name='interior_images', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name

class ProductExteriorImgs(models.Model):
    exterior = models.ImageField(upload_to='exterior', blank=True, null=True)
    product = models.ForeignKey(Products, related_name='exterior_images', on_delete=models.CASCADE)
    def __str__(self):
        return self.product.product_name
    
