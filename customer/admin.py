from django.contrib import admin
from .models import Customer,Loan
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'approved_limit')

class LoanAdmin(admin.ModelAdmin):
    list_display =('customer__customer_id','loan_id','loan_amount','start_date','end_date')

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Loan,LoanAdmin)