from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class income(models.Model):
    income_id = models.AutoField(primary_key=True)
    income_amount = models.CharField(max_length=100)
    income_source = models.CharField(max_length=100)
    income_date = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE , default=0)

