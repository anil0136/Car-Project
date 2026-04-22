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
    return render(request, 'cars/productlist.html', {
        'products': products,
        'company': None
    })

@login_required(login_url='login') 
def product_list(request):
    products = Products.objects.all()
    return render(request, 'cars/productlist.html', {
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
def emi(request):
    annual_interest_rate = 9.5
    car_price = request.GET.get('price') or request.POST.get('car_price') or ""
    car_name = request.GET.get('car') or request.POST.get('car_name') or ""
    down_payment = request.POST.get('down_payment') or ""
    years = request.POST.get('years') or ""
    emi_result = None
    finance_amount = None
    total_payment = None
    total_interest = None
    emi_error = None

    if request.method == 'POST':
        try:
            car_price_value = float(car_price)
            down_payment_value = float(down_payment)
            years_value = int(years)

            if car_price_value <= 0:
                raise ValueError("Car price must be greater than zero.")
            if down_payment_value < 0:
                raise ValueError("Down payment cannot be negative.")
            if down_payment_value >= car_price_value:
                raise ValueError("Down payment must be less than the car price.")
            if years_value <= 0:
                raise ValueError("Loan duration must be at least 1 year.")

            finance_amount = car_price_value - down_payment_value
            total_months = years_value * 12
            monthly_interest_rate = annual_interest_rate / (12 * 100)

            if monthly_interest_rate == 0:
                emi_result = finance_amount / total_months
            else:
                emi_result = (
                    finance_amount
                    * monthly_interest_rate
                    * pow(1 + monthly_interest_rate, total_months)
                ) / (pow(1 + monthly_interest_rate, total_months) - 1)

            total_payment = emi_result * total_months
            total_interest = total_payment - finance_amount
        except (TypeError, ValueError) as exc:
            emi_error = str(exc) if str(exc) else "Enter valid values to calculate EMI."

    return render(request, 'cars/emi.html', {
        'annual_interest_rate': annual_interest_rate,
        'car_price': car_price,
        'car_name': car_name,
        'down_payment': down_payment,
        'years': years,
        'emi_result': emi_result,
        'finance_amount': finance_amount,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'emi_error': emi_error,
    })

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
