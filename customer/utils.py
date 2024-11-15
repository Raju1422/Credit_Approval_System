import datetime
import math

def calculate_credit_score( customer, loans):
        try :
             # for new customer
            if not loans.exists():  
                return 100
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
            return min(credit_score,100)
        except Exception as e:
            print(e)
            return None
        
def determine_approval(customer,loans,credit_score,loan_amount,interest_rate,tenure):
        # for new customer
        if credit_score == 100:
            return True, interest_rate, None
        
        total_current_emis = sum(loan.monthly_installment for loan in loans)
        monthly_salary = customer.monthly_income
        if total_current_emis > 0.5*monthly_salary:
            return False,interest_rate,"Your Total Current Emis are more than your 50 percentage of salary"
        if credit_score > 50 :
            return True,interest_rate,None if interest_rate >= 10 else 10
        elif 30 < credit_score <= 50:
            return True ,max(interest_rate, 12),None
        elif 10 < credit_score <= 30:
            return True,max(interest_rate, 16),None
        else:
            return False,interest_rate,"Your Credit Score is less than 10 (out of 100)"
        
def calculate_monthly_installment(loan_amount, interest_rate, tenure):
        monthly_rate = interest_rate / (12 * 100)
        emi = loan_amount * monthly_rate * math.pow(1 + monthly_rate, tenure) / (math.pow(1 + monthly_rate, tenure) - 1)
        return round(emi, 2)
   