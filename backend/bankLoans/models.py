from django.db import models
from  django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User

from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

CAR = 'Car'
MORTGAGE = 'Mortgage'
PERSONAL = 'Personal'

Loan_Fund_Types = [
    (CAR, 'Car'),
    (MORTGAGE, 'Mortgage'),
    (PERSONAL, 'Personal')
]

MAX_DURATION = 20             # 20 year
MIN_DURATION = 1              # 1 years
MAX_INTEREST_RATE = 30        # 30%
MIN_INTEREST_RATE = 1         # 1%

MIN_LOAN_AMOUNT = 1000
MAX_LOAN_AMOUNT = 1000000
MIN_FUND_AMOUNT = 1000000
MAX_FUND_AMOUNT = 100000000


PENDING = 'Pending'
REJECTED = 'Rejected'
ACCEPTED = 'Accepted'

Application_Status = [
    (PENDING, 'Pending'),
    (REJECTED, 'Rejected'),
    (ACCEPTED, 'Accepted')
]

User_Types = [
    ('Bank Per', 'Bank Personnel'),
    ('PROV', 'Provider'),
    ('CUST', 'Customer')
]
class LoanFund(models.Model):
    min_amount =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_FUND_AMOUNT), 
                                                             MaxValueValidator(MAX_FUND_AMOUNT/10)],blank=False)
    max_amount =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_FUND_AMOUNT*10), 
                                                             MaxValueValidator(MAX_FUND_AMOUNT)],blank=False)
    current_amount =  models.PositiveIntegerField(blank=True, default=0)
    duration =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_DURATION), 
                                                        MaxValueValidator(MAX_DURATION)], blank=False)
    interest_rate =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_INTEREST_RATE), 
                                                             MaxValueValidator(MAX_INTEREST_RATE)], blank=False)
    fund_type = models.CharField(
        max_length=20,
        choices=Loan_Fund_Types,
        default=PERSONAL
    )

    def __str__(self):
        return '{} - {} - {} years - {} IR'.format(self.pk,self.fund_type, self.duration, self.interest_rate)

class Loan(models.Model):
    min_amount =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_LOAN_AMOUNT), 
                                                             MaxValueValidator(MAX_LOAN_AMOUNT/10)],blank=False)
    max_amount =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_LOAN_AMOUNT*10), 
                                                             MaxValueValidator(MAX_LOAN_AMOUNT)],blank=False)
    duration =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_DURATION), 
                                                        MaxValueValidator(MAX_DURATION)],blank=False)
    interest_rate =  models.PositiveIntegerField(validators=[MinValueValidator(MIN_INTEREST_RATE), 
                                                             MaxValueValidator(MAX_INTEREST_RATE)],blank=False)
    loan_fund = models.ForeignKey(LoanFund, related_name='loans', on_delete=models.CASCADE)


    def __str__(self):
        return '{} - {} - {} years - {} IR'.format(self.pk, self.loan_fund.fund_type, self.duration, self.interest_rate)


class LoanFundApplication(models.Model):
    amount = models.PositiveIntegerField(blank=False)
    status = models.CharField(
        max_length=20,
        choices=Application_Status,
        default=PENDING
    )
    loan_fund = models.ForeignKey(LoanFund, related_name='fund_apps', on_delete=models.CASCADE)
    provider = models.ForeignKey(User, related_name='fund_apps', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}$ - {} - by {}'.format(self.pk, self.loan_fund.fund_type, self.amount, self.status, self.provider)


class LoanApplication(models.Model):
    amount = models.PositiveIntegerField(blank=False)
    status = models.CharField(
        max_length=20,
        choices=Application_Status,
        default=PENDING
    )
    loan = models.ForeignKey(Loan, related_name='loan_apps', on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name='loan_apps', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}$ - {} - by {}'.format(self.pk, self.loan.loan_fund.fund_type, self.amount, self.status, self.customer)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20,
        choices=User_Types,
        default='CUST'
    )

