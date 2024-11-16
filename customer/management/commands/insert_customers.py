from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from customer.models import Customer
import pandas as pd
from django.db import transaction
class Command(BaseCommand):
    help = "This is used for inserting Customer data from Excel to Database"

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
                   instance = Customer(
                        first_name=row['First Name'],
                        last_name=row['Last Name'],
                        age=row['Age'],
                        phone_number=str(row['Phone Number']),  
                        monthly_income=float(row['Monthly Salary']),
                        approved_limit=row['Approved Limit']
                    )
                   instances.append(instance)
                if instances:
                    with transaction.atomic():
                        Customer.objects.bulk_create(instances,batch_size=batch_size)
                    instances.clear()
            self.stdout.write(self.style.SUCCESS("Successfully imported Customer data"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))

