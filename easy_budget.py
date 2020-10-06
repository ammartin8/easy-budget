# Pseudo-code
# python packages
from collections import OrderedDict  # keeps options in order we want
import datetime
import os
import sys


# Third-party packages
from peewee import *

# Say welcome to the easy budget app!
print("Welcome to the Easy Budget App! The interactive application that keeps track of all your expenses!")
# Have user select from add item, view items, view chart or quit options:


def menu_loop():
    """Show menu options"""
    menu_choice = None

    while menu_choice != 'q':  # need test case here
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print(f'{key}) {value.__doc__}')
        menu_choice = input(
            "Please choose an option [a,t,c,h]: ").lower().strip()

        if menu_choice in menu:
            menu[menu_choice]()

# add item menu
def add_entry():
    """Add New Record Entry"""
    entry_choice = input("Would you like to add a new expense item or income item? [e/i]: ")
    while True:
        if entry_choice.lower() == 'e':
            add_expense_record()
            break
        elif entry_choice.lower() == 'i':
            add_income_record()
            break

# Add new expense item
def add_expense_record():
    """Add New Expense Record"""
    date_format = '%m/%d/%Y'
    value_type = "expense"
    # Enter Date of Expense - may need unittest here
    while True:
        # TODO: Choose Category
        expense_date = input(
            "Enter the date of the expense. Please use MM/DD/YYYY format. Enter 'q' to quit")
        if expense_date.upper() == 'Q':
            break

        try:
            date = datetime.datetime.strptime(expense_date, date_format)
        except ValueError:
            print("That's not a valid date. Please try again.")
            continue

        try:
            amount = float(
                input("Enter cost amount in $$.$$ format "))
        except ValueError:
            print("That's not a valid cost. Please try again.")
            continue

        item_name = input("Enter item name: ").upper()
        print(
            f"The following record has been saved: \n Item: {item_name}\n Amount: ${amount} \n Date:{date} \n Type: {value_type}")
        cont_choice = input("Would you like to add another item? [y/n] ")
        if cont_choice == 'y':
            continue
        elif cont_choice == 'n':
            break

def add_income_record():
    """Add New Income Record"""
    date_format = '%m/%d/%Y'
    value_type = "income"
    # Enter Date of Income - may need unittest here
    while True:
        income_date = input(
            "Enter the date of the income received. Please use MM/DD/YYYY format. Enter 'q' to quit")
        if income_date.upper() == 'Q':
            break

        try:
            date = datetime.datetime.strptime(income_date, date_format)
        except ValueError:
            print("That's not a valid date. Please try again.")
            continue

        try:
            amount = float(
                input("Enter amount in $$.$$ format "))
        except ValueError:
            print("That's not a valid amount. Please try again.")
            continue

        item_name = input("Enter item name: ").upper()
        print(
            f"The following record has been saved: \n Item: {item_name}\n Amount: ${amount} \n Date:{date} \n Type: {value_type}")
        cont_choice = input("Would you like to add another item? [y/n] ")
        if cont_choice.lower == 'y':
            continue
        elif cont_choice.lower == 'n':
            break


menu = OrderedDict([
    ('a', add_entry),
])

if __name__ == "__main__":
    menu_loop()
