# Generated by Django 3.1.7 on 2021-03-23 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankLoans', '0002_remove_loan_fund_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapplication',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='loanfund',
            name='fund_type',
            field=models.CharField(choices=[('Car', 'Car'), ('Mortgage', 'Mortgage'), ('Personal', 'Personal')], default='Personal', max_length=20),
        ),
        migrations.AlterField(
            model_name='loanfundapplication',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending', max_length=20),
        ),
    ]
