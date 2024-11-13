from rest_framework import serializers
from .models import Customer

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

