from rest_framework import serializers
from customer.models import Loan, Customer
class CustomerRegisterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        read_only_fields = ['customer_id']  
        approved_limit = serializers.FloatField(required=False)
        current_debt = serializers.FloatField(required=False)
        fields = ['customer_id','name' ,'first_name', 'last_name', 'age', 'monthly_income', 'phone_number','approved_limit']

    def create(self, validated_data):
        approved_limit = round(36 * validated_data['monthly_income'] )
        return Customer.objects.create(approved_limit=approved_limit, **validated_data)
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class CheckLoanEligibilitySerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer_id', 'loan_amount', 'interest_rate', 'tenure']

    def validate(self, attrs):
        customer_id = attrs.pop('customer_id') 
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"customer_id": "Customer not found"})
        attrs['customer'] = customer
        return attrs

class CheckEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.FloatField()
    corrected_interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()
    monthly_installment = serializers.FloatField()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'phone_number', 'age']
class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_installment', 'tenure']