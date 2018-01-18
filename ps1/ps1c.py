# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:12:23 2018

@author: Whil

We are now calculating the % of your income to save to get the
downpayment in 36 months.
"""


# Retrieve user input.
annual_salary_init = float(input("Enter your annual salary: "))
annual_return = 0.04
semi_annual_raise = 0.07
total_cost = 350000
portion_down_payment = total_cost * 0.25

# Initialize variables for the bisection search.
low = 0
high = 10000
rate = 0
number_of_months = 36
difference = portion_down_payment
steps = 0
difference = portion_down_payment

while abs(difference) > 100:
    if low == 9999:
        break
    steps += 1
    rate = int((high + low) / 2)
    difference = 0.00
    current_savings = 0.00
    annual_salary = annual_salary_init
    for n in range(36):
        current_savings += current_savings*(annual_return/12)
        current_savings += annual_salary/12.0 * rate/10000.0
        if (n + 1) % 6 == 0:
            annual_salary = annual_salary + (annual_salary * semi_annual_raise)
            
    difference = (current_savings - portion_down_payment)
    if difference < 0:
        low = rate
    else:
        high = rate

if low == 9999:
    print("It is not possible to pay the downpayment in three years.")
else:
    print("Best savings rate:",rate/10000.0)
    print("Steps in bisection:",steps)