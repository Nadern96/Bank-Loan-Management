from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LoanFund)
admin.site.register(Loan)
admin.site.register(LoanApplication)
admin.site.register(LoanFundApplication)
admin.site.register(Account)
