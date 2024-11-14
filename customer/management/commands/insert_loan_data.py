from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from customer.models import Loan,Customer
import pandas as pd
from django.db import transaction
class Command(BaseCommand):
    help = "This is used for inserting Loan data from Excel to Database"

    def add_arguments(self, parser):
        parser.add_argument('file_path',type=str,help='Path to the Excel file')

    def handle(self, *args, **options):
        batch_size = 50
        file_path = options['file_path']
        try :
            data = pd.read_excel(file_path)
            num_rows = data.shape[0]
            for start in range(0,num_rows,batch_size):
                end = start + batch_size
                batch_data = data[start:end]
                instances = []
                for _,row in batch_data.iterrows():
                   customer_instance = Customer.objects.get(customer_id=row['Customer ID'])
                   instance = Loan(
                        customer=customer_instance,
                        loan_id=row['Loan ID'],
                        loan_amount=row['Loan Amount'],
                        tenure=row['Tenure'],
                        interest_rate =row['Interest Rate'],  
                        monthly_installment=row['Monthly payment'],
                        emi_paid=row['EMIs paid on Time'],
                        start_date = row['Date of Approval'],
                        end_date = row['End Date']
                    )
                   instances.append(instance)
                if instances:
                    with transaction.atomic():
                        Loan.objects.bulk_create(instances,batch_size=batch_size)
                    instances.clear()
            self.stdout.write(self.style.SUCCESS("Successfully imported Loan data"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
        except instance.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"Instance not found \n Error : {e}"))

