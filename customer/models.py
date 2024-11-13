from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    monthly_income = models.FloatField() # monthly income  should be Float Field
    phone_number = models.CharField(max_length=15) #Integer Field is not ideal for phone number 
    approved_limit = models.IntegerField(null=True,blank=True)
    current_debt = models.FloatField(default=0.0,blank=True)

    def __str__(self) -> str:
        return f"{self.customer_id} {self.monthly_income}"