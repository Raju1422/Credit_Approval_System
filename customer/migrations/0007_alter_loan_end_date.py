# Generated by Django 5.1.3 on 2024-11-15 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_loan_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
