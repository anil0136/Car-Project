from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRegistation(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    mobile_no=models.PositiveIntegerField()
    door_no=models.PositiveIntegerField()
    street=models.CharField(max_length=100)
    land_mark=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.PositiveIntegerField()
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True, null=True)
    
