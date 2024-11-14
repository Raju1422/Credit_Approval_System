from django.shortcuts import render
from .serializers import CustomerRegisterSerializer,CheckLoanEligibilitySerializer,CheckEligibilityResponseSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Loan
import datetime,math
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

                credit_score=self.calculate_credit_score(customer=customer,loans=loans)
                approval,corrected_interest_rate = self.determine_approval(customer,loans,credit_score,loan_amount,interest_rate,tenure)

                monthly_installment = self.calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)

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
        
    def calculate_credit_score(self, customer, loans):
        try :
            total_loan_amount = 0
            total_loans_tenure_time = 0
            total_emis_paid_on_time = 0
            total_loans = loans.count()
            past_year = datetime.datetime.now().year - 1
            recent_loan_activity = 0
            for loan in loans:
                total_loan_amount+=loan.loan_amount 
                total_loans_tenure_time+=loan.tenure
                total_emis_paid_on_time+=loan.emi_paid
                if loan.start_date.year ==  past_year:
                    recent_loan_activity+=1

            past_loan_score = total_loans * 0.2
            loan_paid_on_time_score = (total_emis_paid_on_time/total_loans_tenure_time)*0.4
            recent_loan_activity_score = recent_loan_activity*0.2
            if total_loan_amount > customer.approved_limit:
                return 0
            else :
                total_loan_amount_score = 0.4
             
            credit_score = (past_loan_score + loan_paid_on_time_score+recent_loan_activity_score+total_loan_amount_score) * 100
            return credit_score
        except Exception as e:
            print(e)
            return None
        
    def determine_approval(self,customer,loans,credit_score,loan_amount,interest_rate,tenure):
        total_current_emis = sum(loan.monthly_installment for loan in loans)
        monthly_salary = customer.monthly_income
        if total_current_emis > 0.5*monthly_salary:
            return False,interest_rate
        if credit_score > 50 :
            return True,interest_rate if interest_rate >= 10 else 10
        elif 30 < credit_score <= 50:
            return True ,max(interest_rate, 12)
        elif 10 < credit_score <= 30:
            return True,max(interest_rate, 16)
        else:
            return False,interest_rate
        
    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        monthly_rate = interest_rate / (12 * 100)
        emi = loan_amount * monthly_rate * math.pow(1 + monthly_rate, tenure) / (math.pow(1 + monthly_rate, tenure) - 1)
        return round(emi, 2)