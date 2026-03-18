from django.shortcuts import render, get_object_or_404
from .models import Company, Products
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login') 
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'cars/companylist.html', {'companies': companies})


@login_required(login_url='login') 
def product_list(request):
    products = Products.objects.all()
    return render(request, 'cars/productslist.html', {
        'products': products,
        'company': None
    })

@login_required(login_url='login') 
def product_list(request):
    products = Products.objects.all()
    return render(request, 'cars/productslist.html', {
        'products': products,
        'company': None
    })

@login_required(login_url='login')
def company_products(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    products = Products.objects.filter(company=company)
    return render(request, 'cars/productlist.html', {
        'products': products,
        'company': company
    })

@login_required(login_url='login')
def emi (request):
    return render(request, 'cars/emi.html',{})

@login_required(login_url='login')
def details1(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    interior_images = product.interior_images.all()
    exterior_images = product.exterior_images.all()
    return render(request, 'cars/details1.html', {
        'product': product,
        'interior_images': interior_images,
        'exterior_images': exterior_images,
    })
