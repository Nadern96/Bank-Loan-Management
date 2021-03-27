from rest_framework import serializers
from .models import LoanFund, Loan, LoanFundApplication, LoanApplication, Account
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.http import JsonResponse


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')    

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_type']

class LoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFund
        fields = ['id', 'min_amount', 'max_amount', 'current_amount', 'duration', 'interest_rate', 'fund_type']

class LoanSerializer(serializers.ModelSerializer):
    loan_fund = LoanFundSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = ['id', 'min_amount', 'max_amount', 'duration', 'interest_rate', 'loan_fund']


class LoanFundApplicationSerializer (serializers.ModelSerializer):
    loan_fund = LoanFundSerializer(read_only=True)
    provider = UserSerializer(read_only=True)
    class Meta:
        model = LoanFundApplication
        fields = ['id', 'amount', 'status', 'loan_fund', 'provider']

      
class LoanApplicationSerializer (serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    customer = UserSerializer(read_only=True)
    class Meta:
        model = LoanApplication
        fields = ['id', 'amount', 'status', 'loan', 'customer']





        