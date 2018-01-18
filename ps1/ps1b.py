# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:12:23 2018

@author: Whil
"""


# Retrieve user input.
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

# Define state variables.
portion_down_payment = total_cost * 0.25
# Rate of return
r = 0.04
current_savings = 0.00
months = 0 

while current_savings <= portion_down_payment:
    current_savings += current_savings * r/12
    current_savings += annual_salary/12 * portion_saved
    months += 1
    if months % 6 == 0:
        annual_salary += annual_salary * semi_annual_raise
    
print("Number of months:", months)
    