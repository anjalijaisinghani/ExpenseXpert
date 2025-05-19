from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class expenses(models.Model):
    expense_id = models.AutoField(primary_key=True)
    expense_name = models.CharField(max_length=100)
    expense_amount = models.CharField(max_length=100)
    expense_category = models.CharField(max_length=100)
    expense_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=0)
    def __str__(self):
        return self.expense_name
    

