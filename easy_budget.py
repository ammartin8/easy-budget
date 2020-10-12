# Pseudo-code
# python packages
from collections import OrderedDict  # keeps options in order we want
import datetime
import os
import sys


# Third-party packages
from peewee import *

db = SqliteDatabase('budgetdata.db')


class Entry(Model):
    ID = AutoField()
    Timestamp = DateTimeField(default=datetime.datetime.now)
    Budget_item_date = DateField(default=datetime.datetime.now)
    Value_type = CharField(default="None")
    Item_name = CharField()
    Amount = DecimalField(decimal_places=2, auto_round=True)
    Category = CharField(default="None")

    class Meta:
        database = db


def initialize():
    """Create a new database if it doesn't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


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
            "Please choose an option: ").strip()

        if menu_choice in menu:
            menu[menu_choice]()


def add_record():
    """Add New Record Entry"""
    while True:
        entry_choice = input(
            "Would you like to add a new expense item or income item? [e/i]: ")  # bug when entering anything other than e/i
        if entry_choice.lower() == 'e':
            add_expense_record()
            break
        elif entry_choice.lower() == 'i':
            add_income_record()
            break
        else:
            print("Not a valid choice. Please try again.")
            continue


def view_records():
    """View List of Budget Items"""
    records = Entry.select().order_by(Entry.Budget_item_date, Entry.Value_type.desc())

    for record in records:
        record = f'{record.ID}) {record.Budget_item_date} \t {record.Item_name} \t {record.Amount} \t {record.Category} {record.Value_type} \t '
        print(record)

    rec_choice = input(
        "Select a number if you want to view a specific record. Enter q to quit to main menu: ")
    while rec_choice.lower() != 'q':
        if rec_choice.lower() in Entry.ID:
            record = Entry.get(Entry.ID == rec_choice)
            # for item in record:
            print(f"ID: {record.ID}")
            print(f"Date: {record.Budget_item_date}")
            print(f"Item: {record.Item_name}")
            print(f"Amount: {record.Amount}")
            print(f"Category: {record.Category}")
            print(f"Type: {record.Value_type} \n\n")

            print("1) Edit this entry")
            print("2) Delete this entry")
            print("Press 'q' to go back to main menu")

            next_choice = input("Please select an option:  ")
            if next_choice.strip(")") == '1':
                edit_record()
                break
            elif next_choice.strip(")") == '2':
                delete_record(record)
                break
            elif next_choice.lower().strip() == 'q':
                break



def edit_record():
    """Edit A Record"""
    pass


def delete_record(record):
    """Delete A Record"""
    if input("Are you sure? [y/n]").lower() == 'y':
        record.delete_instance()
        print("Record Deleted!")


def add_expense_record():
    """Add New Expense Record"""
    date_format = '%m/%d/%Y'
    value_type = "expense"
    # Enter Date of Expense - may need unittest here
    while True:
        # Choose a Category
        for key, value in expense_categories.items():
            print(f'{key}) {value}')
        category_choice = input(
            "Choose an Expense Category or Enter 'q' to quit. ").strip()
        if category_choice.upper() == 'Q':
            break

        if category_choice in expense_categories:
            category = expense_categories[category_choice]

        expense_date = input(
            "Enter the date of the expense. Please use MM/DD/YYYY format. ")

        try:
            budget_item_date = datetime.datetime.strptime(
                expense_date, date_format)
        except ValueError:
            print("That's not a valid date. Please try again.")
            continue

        try:  # test negative values
            amount = round(float(
                input("Enter cost amount in $$.$$ format ")), 2)
        except ValueError:
            print("That's not a valid cost. Please try again.")
            continue

        item_name = input("Enter item name: ").upper()
        print(
            f"The following record has been entered: \n Item: {item_name}\n Amount: ${amount} \n Date:{budget_item_date} \n Category={category} Type: {value_type}")

        save_choice = input("Would you like to save? [y/n]: ")
        if save_choice.lower() != 'n':
            Entry.create(Budget_item_date=budget_item_date, Item_name=item_name,
                         Amount=amount, Category=category, Value_type=value_type)
            print("Record Saved!")
        else:
            print("Entry not saved")

        cont_choice = input("Would you like to add another item? [y/n] ")
        if cont_choice.lower() == 'y':
            continue
        elif cont_choice.lower() == 'n':
            break


def add_income_record():
    """Add New Income Record"""
    date_format = '%m/%d/%Y'
    value_type = "income"

    while True:
        # Choose a Category
        for key, value in income_categories.items():
            print(f'{key}) {value}')
        category_choice = input("Choose an Income Category: ").strip()

        if category_choice in income_categories:
            category = income_categories[category_choice]

          # Enter Date of Income - may need unittest here
        income_date = input(
            "Enter the date of the income received. Please use MM/DD/YYYY format. Enter 'q' to quit")
        if income_date.upper() == 'Q':
            break

        try:
            budget_item_date = datetime.datetime.strptime(
                income_date, date_format)
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
            f"The following record has been entered: \n Item: {item_name}\n Amount: ${amount} \n Date:{budget_item_date} \n Category: {category} Type: {value_type}")

        save_choice = input("Would you like to save? [y/n]: ")
        if save_choice.lower() != 'n':
            Entry.create(Budget_item_date=budget_item_date, Item_name=item_name,
                         Amount=amount, Category=category, Value_type=value_type)
            print("Record Saved!")
        else:
            print("Entry not saved")

        cont_choice = input("Would you like to add another item? [y/n] ")
        if cont_choice.lower() == 'y':
            continue
        elif cont_choice.lower() == 'n':
            break


menu = OrderedDict([
    ('1', add_record),
    ('2', view_records),
    # ('3', delete_record),
])

expense_categories = OrderedDict([
    ('1', 'Transportation'),
    ('2', 'Housing'),
    ('3', 'Food'),
    ('4', 'Lifestyle'),
    ('5', 'Insurance & Tax'),
    ('6', 'Business'),
    ('7', 'Miscellaneous'),
])

income_categories = OrderedDict([
    ('1', 'Employer'),
    ('2', 'Business'),
    ('3', 'Hobby'),
    ('4', 'Other'),
])

if __name__ == "__main__":
    initialize()
    menu_loop()
