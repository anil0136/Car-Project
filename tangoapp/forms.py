from django.contrib.auth.models import User
from .models import UserRegistation
from django import forms
from django_recaptcha.fields import ReCaptchaField

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','email','password']
    
class UserDetails(forms.ModelForm):
    class Meta:
        model=UserRegistation
        fields=['mobile_no','door_no','street','land_mark','city','state','pincode','profile_pic']
    captcha = ReCaptchaField()

class UserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']
class UserUpdate1(forms.ModelForm):
    class Meta:
        model=UserRegistation
        fields=['mobile_no','door_no','street','land_mark','city','state','pincode']

class PasswordReset(forms.Form):
    user_name = forms.CharField(max_length=100)
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    conform_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
