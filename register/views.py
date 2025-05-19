from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def register_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if(password != confirm_password):
            messages.error(request,"Password and Confirm Password must match")
            return redirect('../register/')
        else: 
            try:
                user = User.objects.create(
                    username = username,
                    email =email,
                    password =password,
                    is_active = False,
                )
                user.save()
                messages.success(request,"User Registered Successfully ! Please Login")
                return redirect('../login/')
            except Exception as e:
                print("User Not Created : ",e)

    return render(request,'register.html')