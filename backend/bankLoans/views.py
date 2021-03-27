from django.shortcuts import render
from .models import LoanFund, Loan, LoanFundApplication, LoanApplication, Account
from .models import PENDING, REJECTED, ACCEPTED 
from .serializers import LoanFundSerializer, LoanSerializer, LoanFundApplicationSerializer, LoanApplicationSerializer
from .serializers import UserSerializer, AccountSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from amortization.schedule import amortization_schedule
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'loanfunds': reverse('loanfund-list', request=request, format=format),
        'loan': reverse('loan-list', request=request, format=format),
        'loanfundapps': reverse('loanfundapp-list', request=request, format=format),
        
    })

# Loan Fund
class LoanFundList(generics.ListCreateAPIView):
    queryset = LoanFund.objects.all()
    serializer_class = LoanFundSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, format=None):
        serializer = LoanFundSerializer(data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to create a loan fund' 
            return Response(error)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanFundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanFund.objects.all()
    serializer_class = LoanFundSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return LoanFund.objects.get(pk=pk)
        except LoanFund.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk, format=None):
        loanfund = self.get_object(pk)
        serializer = LoanFundSerializer(loanfund)
        return Response(serializer.data)

    def update(self, request, pk, format=None):
        loanfund = self.get_object(pk)
        serializer = LoanFundSerializer(loanfund, data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to update loan fund details' 
            return Response(error)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        loanfund = self.get_object(self.kwargs.get('pk'))
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to delete a loan fund' 
            return Response(error)

        loanfund.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Loan
class LoanList(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, format=None):
        serializer = LoanSerializer(data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to create a loan' 
            return Response(error)

        if serializer.is_valid():
            loanfund = LoanFund.objects.get(pk=request.data['loan_fund'])
            if (serializer.validated_data['min_amount'] > loanfund.min_amount 
                or serializer.validated_data['max_amount'] > loanfund.min_amount):
                error['error'] = 'Min and Max amount must be less than ' + str(loanfund.min_amount)
                return Response(error)

            serializer.save(loan_fund=loanfund)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk, format=None):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan)
        return Response(serializer.data)

    def update(self, request, pk, format=None):
        loan = self.get_object(pk)
        serializer = LoanSerializer(loan, data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to update a loan' 
            return Response(error)

        if serializer.is_valid():
            if (serializer.validated_data['min_amount'] > loanfund.min_amount 
                or serializer.validated_data['max_amount'] > loanfund.min_amount):
                error['error'] = 'Min and Max amount must be less than ' + str(loanfund.min_amount)
                return Response(error)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        loan = self.get_object(self.kwargs.get('pk'))
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to delete a loan' 
            return Response(error)

        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Loan Fund Application
class LoanFundAppList(generics.ListCreateAPIView):
    queryset = LoanFundApplication.objects.all()
    serializer_class = LoanFundApplicationSerializer

    def list(self, request, format=None):
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type == 'Bank Per':
            loanFundApps = LoanFundApplication.objects.all()
            serializer = LoanFundApplicationSerializer(loanFundApps, many=True)
            return Response(serializer.data)

        loanFundApps = LoanFundApplication.objects.filter(provider=request.user)
        serializer = LoanFundApplicationSerializer(loanFundApps, many=True)
        return Response(serializer.data)

            
    def create(self, request, format=None):
        serializer = LoanFundApplicationSerializer(data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        if account.user_type == 'PROV':
            if serializer.is_valid():

                loanfund = LoanFund.objects.get(pk=request.data['loan_fund'])
                if (serializer.validated_data['amount'] >= loanfund.min_amount 
                    and serializer.validated_data['amount'] <= loanfund.max_amount):

                    # set application status intially to Pending 
                    serializer.validated_data['status'] = PENDING
                    serializer.save(provider=request.user, loan_fund=loanfund)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    error['error'] = 'Amount must be more than ' + str(loanfund.min_amount) + ' and less than ' + str(loanfund.max_amount) 
                    return Response(error)
        else:
            error['error'] = 'Only Providers are allowed to apply for a loan fund application' 
            return Response(error)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanFundAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanFundApplication.objects.all()
    serializer_class = LoanFundApplicationSerializer

    def get_object(self, pk):
        try:
            return LoanFundApplication.objects.get(pk=pk)
        except LoanFundApplication.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk, format=None):
        loanFundApp = self.get_object(pk)
        serializer = LoanFundApplicationSerializer(loanFundApp)

        user = User.objects.get(id=request.user.id)
        error = {}

        if user.id != serializer.data['provider']['id'] and user.account.user_type != 'Bank Per':
            error['error'] = 'You are not allowed to view this loan fund application' 
            return Response(error)
        
        serializer = LoanFundApplicationSerializer(loanFundApp)
        return Response(serializer.data)

    def update(self, request, pk, format=None):
        loanFundApp = self.get_object(pk)
        request.data['amount'] = loanFundApp.amount
        serializer = LoanFundApplicationSerializer(loanFundApp, data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to update the loan fund application details' 
            return Response(error)

        if serializer.is_valid():
            if serializer.validated_data['status'] == ACCEPTED:
                loanfund = LoanFund.objects.get(pk=loanFundApp.loan_fund.pk)
                loanfund.current_amount += serializer.validated_data['amount']
                loanfund.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to delete the loan fund application' 
            return Response(error)

        loanFundApp = self.get_object(self.kwargs.get('pk'))
        loanFundApp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Loan Application
class LoanAppList(generics.ListCreateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer

    def list(self, request, format=None):
        account = Account.objects.get(user=request.user)
        error = {}

        if account.user_type == 'Bank Per':
            loanApps = LoanApplication.objects.all()
            serializer = LoanApplicationSerializer(loanApps, many=True)
            return Response(serializer.data)

        loanApps = LoanApplication.objects.filter(customer=request.user)
        serializer = LoanApplicationSerializer(loanApps, many=True)
        return Response(serializer.data)


    def create(self, request, format=None):
        serializer = LoanApplicationSerializer(data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        if account.user_type == 'CUST':

            if serializer.is_valid():
                print("hellooo")

                loan = Loan.objects.get(pk=request.data['loan'])
                if (serializer.validated_data['amount'] >= loan.min_amount 
                    and serializer.validated_data['amount'] <= loan.max_amount):
                    
                    # set application status intially to Pending 
                    serializer.validated_data['status'] = PENDING
                    serializer.save(customer=request.user, loan=loan)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    error['error'] = 'Amount must be more than ' + str(loan.min_amount) + ' and less than ' + str(loan.max_amount) 
                    return Response(error)
        else:
            error['error'] = 'Only Customers are allowed to apply for a loan application' 
            return Response(error)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer

    def get_object(self, pk):
        try:
            return LoanApplication.objects.get(pk=pk)
        except LoanApplication.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk, format=None):
        loanApp = self.get_object(pk)
        serializer = LoanApplicationSerializer(loanApp)

        user = User.objects.get(id=request.user.id)
        error = {}

        if user.id != serializer.data['customer']['id'] and user.account.user_type != 'Bank Per':
            error['error'] = 'You are not allowed to view this loan application' 
            return Response(error)
        
        serializer = LoanApplicationSerializer(loanApp)
        return Response(serializer.data)

    def update(self, request, pk, format=None):
        loanApp = self.get_object(pk)
        request.data['amount'] = loanApp.amount
        serializer = LoanApplicationSerializer(loanApp, data=request.data)
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to update the loan application details' 
            return Response(error)
        
        if serializer.is_valid():
            if serializer.validated_data['status'] == ACCEPTED:

                loanfund = LoanFund.objects.get(pk=loanApp.loan.loan_fund.pk)
                loanfund.current_amount -= serializer.validated_data['amount']
                loanfund.save()

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        account = Account.objects.get(user=request.user)
        error = {}
        
        if account.user_type != 'Bank Per':
            error['error'] = 'Only Bank Personnel are allowed to delete the loan application' 
            return Response(error)

        loanApp = self.get_object(self.kwargs.get('pk'))
        loanApp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Amortization Table
def calcAmorizationTable(amount, iR, period):
    amortization_table = []    

    for number, amount, interest, principal, balance in amortization_schedule(amount, iR*0.01, period*12):        
        amortization_table.append({
            'period': number,
            'amount': amount, 
            'interest': interest, 
            'principal': principal, 
            'balance': balance
        })
    return amortization_table

@api_view(['GET'])
def calcLoanFundAmortization(request, pk):
    """
    Calc amortization table for the loan fund application
    """
    loanFund_app = LoanFundApplication.objects.get(pk=pk)
    serializer = LoanFundApplicationSerializer(loanFund_app)

    if loanFund_app.status != ACCEPTED:
        error = {}
        error['error'] = 'Your application is not accepted yet!' 
        return Response(error)
    
    amortization_table = calcAmorizationTable(loanFund_app.amount, loanFund_app.loan_fund.interest_rate, loanFund_app.loan_fund.duration)
    return Response(amortization_table)

@api_view(['GET'])
def calcLoanAmortization(request, pk):
    """
    Calc amortization table for the loan application
    """
    loan_app = LoanApplication.objects.get(pk=pk)
    serializer = LoanApplicationSerializer(loan_app)

    if loan_app.status != ACCEPTED:
        error = {}
        error['error'] = 'Your application is not accepted yet!' 
        return Response(error)

    print(loan_app.amount, loan_app.loan.interest_rate,loan_app.loan.duration)
    amortization_table = calcAmorizationTable(loan_app.amount, 
                                                loan_app.loan.interest_rate, 
                                                loan_app.loan.duration)
    return Response(amortization_table)

# for token authentication: to-do --> vuetify ui 
class Registration(APIView):
    """ 
    Creates the user. 
    """
    permission_classes = []

    def post(self, request, format='json'):
        user_serializer = UserSerializer(data=request.data)
        account_serializer = AccountSerializer(data=request.data)
        if user_serializer.is_valid() and account_serializer.is_valid():
            user = user_serializer.save()
            print(user)
            account = account_serializer.save(user=user)
            if user:
                token = Token.objects.create(user=user)
                json = user_serializer.data
                json['user_type'] = account_serializer.data['user_type']
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# override the default rest login 

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        return Response({'token': token.key, 'username': token.user.username, 'user_type': token.user.account.user_type})