from django.urls import path
from .views import CustomerRegisterView,CheckEligibilityView,CreateLoanView,LoanDetailsView,CustomerLoanDetailView


urlpatterns = [
    path('register/',CustomerRegisterView.as_view(),name="register"),
    path('check-eligibility/',CheckEligibilityView.as_view(),name="check-eligibility"),
    path('create-loan/',CreateLoanView.as_view(),name="create-loan"),
    path('view-loan/<int:loan_id>/',LoanDetailsView.as_view(),name="view-loan"),
    path('view-loans/<int:customer_id>/',CustomerLoanDetailView.as_view(),name="view-customer-loans")
]
