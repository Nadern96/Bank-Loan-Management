from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/', views.api_root),
    path('api/register/', views.Registration.as_view(), name='register'),
    path('api/login/', views.CustomObtainAuthToken.as_view(), name='login'),


    path('api/loanfunds/', views.LoanFundList.as_view(), name='loanfund-list'),
    path('api/loanfunds/<int:pk>/', views.LoanFundDetail.as_view(), name='loanfund-detail'),
    path('api/loans/', views.LoanList.as_view(), name='loan-list'),
    path('api/loans/<int:pk>/', views.LoanDetail.as_view(), name='loan-detail'),
        
    path('api/loanfundapps/', views.LoanFundAppList.as_view(), name='loanfundapp-list'),
    path('api/loanfundapps/<int:pk>/', views.LoanFundAppDetail.as_view(), name='loanfundapp-detail'),
    
    path('api/loanapps/', views.LoanAppList.as_view(), name='loanapp-list'),
    path('api/loanapps/<int:pk>/', views.LoanAppDetail.as_view(), name='loanapp-detail'),

    path('api/loanfundapps/<int:pk>/amortization/', views.calcLoanFundAmortization, name='loanFund-amortization'),
    path('api/loanapps/<int:pk>/amortization/', views.calcLoanAmortization, name='loan-amortization'),
]
