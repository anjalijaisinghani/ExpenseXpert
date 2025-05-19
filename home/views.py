from django.shortcuts import render
from . import models
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date

def home_views(request):
    expenses = []  # Initialize an empty list for expenses in case no user is logged in.

    if request.method == 'POST':
        expense_name = request.POST.get('expense_name')
        expense_amount = request.POST.get('expense_amount')
        expense_category = request.POST.get('expense_category')
        expense_date = request.POST.get('expense_date')

        try:
            # Get the user based on the email in the session
            email = request.session.get('email')
            if email:
                user = User.objects.get(email=email)
                # Create and save the new expense entry
                expense = models.expenses.objects.create(
                    expense_name=expense_name,
                    expense_amount=expense_amount,
                    expense_category=expense_category,
                    expense_date=expense_date,
                    user=user,
                )
                expense.save()
                messages.success(request, "Expense saved successfully!")
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
            expenses = models.expenses.objects.filter(user=user, expense_date = date.today())
        except User.DoesNotExist:
            messages.error(request, "User not found. Please log in again.")

    # Render the page with the expenses
    return render(request, 'home.html', {'expenses': expenses})
