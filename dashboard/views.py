import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.db.models import Sum
from home.models import expenses
from income.models import income
from django.contrib.auth.models import User

def multiple_charts(request):
    # Get date range from GET parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    email=request.session.get('email')
    user=User.objects.get(email=email)
    # Filter data by date range if provided
    expense_query = expenses.objects.filter(user=user)
    income_query = income.objects.filter(user=user)
    if start_date and end_date:
        expense_query = expense_query.filter(expense_date__range=[start_date, end_date])
        income_query = income_query.filter(income_date__range=[start_date, end_date])

    # Data for Chart 1: Expenses vs. Incomes Over Time
    Exp = expense_query.extra(select={'month': "strftime('%%Y-%%m', expense_date)"}).values('month').annotate(total=Sum('expense_amount')).order_by('month')
    incomes = income_query.extra(select={'month': "strftime('%%Y-%%m', income_date)"}).values('month').annotate(total=Sum('income_amount')).order_by('month')

    months = [item['month'] for item in Exp]
    expense_data = [item['total'] for item in Exp]
    income_data = [item['total'] for item in incomes]
    total_sum_exp = 0
    for i in expense_data:
        total_sum_exp += i
    if len(expense_data) == 0 or len(income_data)==0:
        pass
    else:
         # Chart 1: Expenses vs. Incomes
        plt.figure(figsize=(10, 6))
        plt.plot(months, expense_data, label='Expenses', marker='o', color='red')
        plt.plot(months, income_data, label='Incomes', marker='o', color='blue')
        plt.title('Monthly Expenses vs Incomes')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart1 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # Chart 2: Expense Category Breakdown
        categories = expense_query.values('expense_category').annotate(total=Sum('expense_amount')).order_by('-total')
        category_labels = [item['expense_category'] for item in categories]
        category_data = [item['total'] for item in categories]

        plt.figure(figsize=(8, 8))
        plt.pie(category_data, labels=category_labels, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Category Breakdown')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart2 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        expense_totals = [{'category': item['expense_category'], 'total': item['total']} for item in categories]

        
        # Pass both charts and the current date range to the template
        return render(request, 'multiple_charts.html', {
            'chart1': chart1,
            'chart2': chart2,
            'start_date': start_date,
            'end_date': end_date,
            'expense': expense_query,
            'income':income_query,
            'expense_totals': expense_totals,
            'total_sum_exp': total_sum_exp,
                
        })
    return render(request,'multiple_charts.html',{
        'msg':'msg',
    })