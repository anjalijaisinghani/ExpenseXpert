from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
def logout_view(request):
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])
        user.is_active = False
        del request.session['email']
    return redirect('../home/')
