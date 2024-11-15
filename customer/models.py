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
    

class Loan(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='loans')
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField(null=True,blank=True)
    emi_paid = models.IntegerField(default=0,blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)

    def __str__(self) -> str:
        return f"{self.customer.customer_id} {self.loan_id} {self.loan_amount}"