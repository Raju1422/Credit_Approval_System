from django.shortcuts import render
from .serializers import CustomerRegisterSerializer,CheckLoanEligibilitySerializer,CheckEligibilityResponseSerializer,LoanSerializer,CustomerLoanSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Loan,Customer
import datetime,math
from .utils import calculate_credit_score,determine_approval,calculate_monthly_installment
from django.db import transaction
from django.http import Http404
class CustomerRegisterView(APIView):
    def post(self,request):
        try :
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                data.pop('first_name', None) 
                data.pop('last_name', None) 
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckEligibilityView(APIView):
    def post(self,request):
        try :
            serializer = CheckLoanEligibilitySerializer(data=request.data)
            if serializer.is_valid():

                data = serializer.validated_data
                tenure = data['tenure']
                interest_rate = data['interest_rate']
                loan_amount = data['loan_amount']
                customer = data['customer']
                
                loans = Loan.objects.filter(customer=customer)

                credit_score=calculate_credit_score(customer=customer,loans=loans,loan_amount=loan_amount)
                print(credit_score)
                approval,corrected_interest_rate,message =determine_approval(customer,loans,credit_score,loan_amount,interest_rate,tenure)

                monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)

                response_data = {
                    "customer_id": customer.customer_id,
                    "approval": approval,
                    "interest_rate": interest_rate,
                    "corrected_interest_rate": corrected_interest_rate,
                    "tenure": tenure,
                    "monthly_installment": monthly_installment
                }
                response_serializer = CheckEligibilityResponseSerializer(data=response_data)
                if response_serializer.is_valid():
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CreateLoanView(APIView):
    def post(self,request):
        try :
            serializer = CheckLoanEligibilitySerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                tenure = data['tenure']
                interest_rate = data['interest_rate']
                loan_amount = data['loan_amount']
                customer = data['customer']
                
                loans = Loan.objects.filter(customer=customer)
                credit_score = calculate_credit_score(customer=customer, loans=loans,loan_amount=loan_amount)
                approval, corrected_interest_rate, message = determine_approval(
                    customer, loans, credit_score, loan_amount, interest_rate, tenure
                )

                monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)

                response_data = {
                    "loan_id": None,  
                    "customer_id": customer.customer_id,
                    "loan_approved": approval,
                    "message": message,
                    "monthly_installment": monthly_installment,
                }
                with transaction.atomic():
                    if approval:
                        loan = Loan.objects.create(
                            customer=customer,
                            loan_amount=loan_amount,
                            interest_rate=corrected_interest_rate,
                            tenure=tenure,
                            monthly_installment=monthly_installment,
                        )
                        response_data["loan_id"] = loan.loan_id 
                    return Response(response_data, status=status.HTTP_200_OK)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoanDetailsView(APIView):
    def get_object(self, loan_id):
        try:
            return Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            raise Http404
        
    def get(self, request, loan_id, format=None):
        try :
            loan = self.get_object(loan_id)
            serializer = LoanSerializer(loan)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CustomerLoanDetailView(APIView):
    def get_object(self, customer_id):
        try:
            return Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            raise Http404
        
    def get(self,request,customer_id,format=None):
        try :
            customer = self.get_object(customer_id=customer_id)
            loans = Loan.objects.filter(customer=customer)
            if not loans:
                return Response({"message": "No loans found for this customer."}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerLoanSerializer(loans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
        
