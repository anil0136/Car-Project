from django.shortcuts import render
from .models import Cars
from tangoapp.utils import send_email_view
from django.http import HttpResponse

# Create your views here.
def rent(request):
    seat_type = request.GET.get('seat')
    cars = None
    if seat_type in ['5 seater', '7 seater']:
        cars = Cars.objects.filter(seat_capacity=seat_type)
    return render(request, 'rent/rent.html', {'cars': cars, 'seat_type': seat_type})

def details(request, car_id):
    car = Cars.objects.get(id=car_id)
    return render(request, 'rent/details.html', {'car': car})

def check(request, car_id):
    cal=False
    car = Cars.objects.get(id=car_id)
    km=0
    if car.seat_capacity == '5 seater':
        km=50
    elif car.seat_capacity == '7 seater':
        km=100

    if request.method == 'POST':
        days = int(request.POST.get('days', 1))
        except_km = int(request.POST.get('exp_km', 0))
        if except_km==0:
            total_rent = days * 300 * km 
            print(total_rent)
            cal=True
            return render(request, 'rent/check.html', {'car': car,
                                                   'km': km,
                                                   'days': days,
                                                   'total_rent': total_rent,
                                                   'cal': cal})
        
        else:
            total_rent = except_km*km
            print(total_rent)
            cal=True

            return render(request, 'rent/check.html', {'car': car,
                                                   'km': km,
                                                   'days': days,
                                                   'except_km': except_km,
                                                   'total_rent': total_rent,
                                                   'cal': cal})

            
        

        
    return render(request, 'rent/check.html',{'car': car,
                                              'km': km})

def frent(request,car_id):
    ca = False
    car = Cars.objects.get(id=car_id)
    car_name = car.car_name
    total_km_driven = car.total_km_driven
    total_amount = 0
    user_email = None
    if request.user.is_authenticated:
        user_email = request.user.email
    km = 0
    fp = 0
    if car.seat_capacity == '5 seater':
        km = 50
    elif car.seat_capacity == '7 seater':
        km = 100

    if request.method == 'POST':
        days = int(request.POST.get('days', 1))
        except_km = int(request.POST.get('exp_km', 0))

        tk = except_km - car.total_km_driven
        if tk < 0:
            tk = 0

        petrol = 0
        if car.milage and car.milage != 0:
            petrol = (tk / car.milage) * 102

        if tk > days * 300:
            tp = tk * km
            fp = (tp - petrol) + (tp * 0.02)
        elif tk == days * 300:
            tp = tk * km
            fp = tp - petrol
        else:
            tp = days * 300 * km
            fp = tp - petrol

        total_amount = round(fp, 2)
        ca = True
        if user_email:
            send_email_view(user_email, car_name, total_km_driven, total_amount)
            print("Email sent to:", user_email)

        return render(request, 'rent/frent.html', {'ca': ca, 'km': km, 'car': car, 'fp': total_amount})

    return render(request, 'rent/frent.html', {'ca': ca, 'km': km, 'car': car, 'fp': fp})
