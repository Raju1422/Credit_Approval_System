import datetime
import math

def calculate_credit_score(customer, loans,loan_amount):
    try:
        # For a new customer (no loans), return a perfect score of 100
        if not loans.exists():
            return 100

        # Initialize variables
        total_loan_amount = 0
        total_loans_tenure_time = 0
        total_emis_paid_on_time = 0
        total_loans = loans.count()
        recent_loan_activity = 0
        past_year = datetime.datetime.now().year - 1
        current_year_loans = 0

        # Calculate total loan amount for the customer and check conditions
        for loan in loans:
            total_loan_amount += loan.loan_amount
            total_loans_tenure_time += loan.tenure
            total_emis_paid_on_time += loan.emi_paid

            # Check for loan activity in the current year (past year)
            if loan.start_date.year == past_year:
                recent_loan_activity += 1
            # Check for loans taken in the current year
            if loan.start_date.year == datetime.datetime.now().year:
                current_year_loans += 1

        # 1. Past Loans Paid on Time - 50% threshold
        if (total_emis_paid_on_time / total_loans_tenure_time) > 0.5:
            past_loans_score = 20
        else:
            past_loans_score = 0

        # 2. Number of Loans Taken in the Past - 50% threshold
        if total_loans < 5:
            loans_taken_score = 20
        else:
            loans_taken_score = 0

        if recent_loan_activity < 0.5 * total_loans:
            recent_loan_activity_score = 20
        else:
            recent_loan_activity_score = 0
        if loan_amount > customer.approved_limit :
            loan_amount_score = 0
        else :
            loan_amount_score = 20
        if total_loan_amount > customer.approved_limit:
            return 0
        else :
            approved_loan_volume_score = 20

        credit_score = (past_loans_score + loans_taken_score + loan_amount_score+
                        recent_loan_activity_score + approved_loan_volume_score) 

        return min(credit_score, 100)

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
   