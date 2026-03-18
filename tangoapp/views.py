from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,UserDetails,UserUpdate,UserUpdate1,PasswordReset
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    registered = False
    if request.method=='POST':
        form=UserForm(request.POST)
        form1=UserDetails(request.POST,request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            details = form1.save(commit=False)
            details.user = user
            details.save()
            registered = True

            print(form.cleaned_data['username'])
            print(form1.cleaned_data['mobile_no'])
        
    else:
        form=UserForm()
        form1=UserDetails()
    context={
        'form':form,
        'form1':form1
        ,'registered':registered
        }


    return render(request,'register.html',context)
def user_login(request):

    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username)
        print(password)
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect("home")
        else:
            return HttpResponse("pls check your creda...!")
    return render(request,'login.html',{})
@login_required(login_url='login')
def home(request):
    context={
        'username':request.user.username
    }
    return render(request,"home.html",context)


@login_required(login_url='login')
def profile(request):
    return render(request,"profile.html",{})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_update(request):
    if request.method=='POST':
        form=UserUpdate(request.POST,instance=request.user)
        form1=UserUpdate1(request.POST,instance=request.user.userregistation)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            return redirect('profile')
    else:
        form=UserUpdate(instance=request.user)
        form1=UserUpdate1(instance=request.user.userregistation)
    context={
        'form':form,
        'form1':form1
        }
    return render(request,'update.html',context)
@login_required(login_url='login')
def reset(request):
    form=PasswordReset()
    if request.method=='POST':
        form=PasswordReset(request.POST)
        if form.is_valid():
            username=form.cleaned_data['user_name']
            
            new_password=form.cleaned_data['new_password']
            conform_password=form.cleaned_data['conform_password']
            user=authenticate(username=username)
            try:
                if user and new_password==conform_password: 
                    user.set_password(new_password)
                    user.save()
                    return redirect('login')
            except Exception as e:
                print(e)
            
    return render(request,'reset.html',{'form':form})
