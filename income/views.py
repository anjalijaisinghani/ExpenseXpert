from django.shortcuts import render
from django.contrib.auth.models import User
from . import models
from django.contrib import messages
from datetime import date
# Create your views here.
def income_views(request):
    income = []
    if request.method == 'POST':
        income_source = request.POST.get('income_source')
        income_amount = request.POST.get('income_amount')
        income_date = request.POST.get('income_date')

        try:
            # Get the user based on the email in the session
            email = request.session.get('email')
            if email:
                user = User.objects.get(email=email)
                # Create and save the new expense entry
                income = models.income.objects.create(
                    income_amount=income_amount,
                    income_source=income_source,
                    income_date=income_date,
                    user=user,
                )
                income.save()
                messages.success(request, "Income saved successfully!")
            else:
                messages.error(request, "User is not logged in.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    # Ensure that the user is logged in and fetch their expenses
    if request.session.get('email'):
        email = request.session.get('email')
        try:
            user = User.objects.get(email=email)
            income = models.income.objects.filter(user=user, income_date = date.today())
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")

    return render(request,'income.html',{'income':income})