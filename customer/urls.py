from django.urls import path
from .views import CustomerRegisterView,CheckEligibilityView


urlpatterns = [
    path('register/',CustomerRegisterView.as_view(),name="register"),
    path('check-eligibility/',CheckEligibilityView.as_view(),name="check-eligibility")
]
