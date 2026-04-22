from django.db import models

# Create your models here.
fuel=[
        ('petrol','PETROL'),
        ('diesel',"DIESEL"),
        ('ev','EV')

]
seat=[
        ('5 seater','5 seater'),
        ('7 seater','7 seater')

]
tst=[
        ('manual','MANUAL'),
        ('automated','AUTOMATED')
]

class Cars(models.Model):
    car_name=models.CharField(max_length=100)
    Company=models.CharField(max_length=100)
    color=models.CharField(max_length=100)
    fuel_type=models.CharField(max_length=100,choices=fuel) 
    seat_capacity=models.CharField(max_length=100,choices=seat)
    transmission_type=models.CharField(max_length=100,choices=tst)
    total_km_driven=models.IntegerField()
    amminities=models.CharField(max_length=100)
    bootspace=models.IntegerField()
    rating=models.IntegerField()
    car_img=models.ImageField(upload_to='carimag',blank=True,null=True)
    milage=models.IntegerField()


    def __str__(self):
        return self.car_name
