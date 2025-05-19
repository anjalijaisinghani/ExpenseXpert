from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if(user.password == password):
                user.is_active=True
                
                request.session['email'] = email
                return redirect('../home')
            else:
                
                return redirect('../login')
        except Exception as e:
            
            return redirect('../login') 

    return render(request,'login.html')