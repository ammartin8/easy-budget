# Pseudo-code
# python packages
from collections import OrderedDict  # keeps options in order we want
from prettytable import PrettyTable, from_db_cursor
import datetime
import os
import sys


# Third-party packages
from peewee import *

db = SqliteDatabase('budgetdata.db')


class Entry(Model):
    id = AutoField()
    Timestamp = DateTimeField(default=datetime.datetime.now)
    budget_item_date = DateField(
        default=datetime.datetime.now, verbose_name="date")
    value_type = CharField(default="None")
    item_name = CharField()
    amount = DecimalField(decimal_places=2, auto_round=True)
    category = CharField(default="None")

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
    cursor = db.execute_sql(
        "SELECT id as ID, budget_item_date as Date, item_name as Item, amount as Amount, category as Category FROM entry")
    myTable = from_db_cursor(cursor)
    print(myTable)

    rec_choice = input(
        "Select a number if you want to view a specific record. Enter q to quit to main menu: ")
    while rec_choice.lower() != 'q':
        try:
            if rec_choice.lower() in Entry.id:
                record = Entry.get(Entry.id == rec_choice)
                print(f"id: {record.id}")
                print(f"Date: {record.budget_item_date}")
                print(f"Item: {record.item_name}")
                print(f"Amount: {record.amount}")
                print(f"Category: {record.category}")
                print(f"Type: {record.value_type} \n\n")

                print("1) Edit this entry")
                print("2) Delete this entry")
                print("Press 'q' to go back to main menu")

                next_choice = input("Please select an option:  ")
                if next_choice.strip(")") == '1':
                    edit_record(record)
                    break
                elif next_choice.strip(")") == '2':
                    delete_record(record)
                    break
                elif next_choice.lower().strip() == 'q':
                    break
        except:
            print("Not a valid option. Please try again.")
            break


def edit_record(record):
    """Edit A Record"""
    date_format = '%m/%d/%Y'
    # rec_columns = record._meta.fields
    # for num, cols in enumerate(rec_columns, start=1):
    #     print(num, cols.upper())
    print(f"Date: {record.budget_item_date}")
    print(f"Item: {record.item_name}")
    print(f"Amount: {record.amount}")
    print(f"Category: {record.category}")
    print(f"Type: {record.value_type} \n\n")

    column_choice = input(
        "What field do you want to edit? ")

    if column_choice == "date":
        date_update_input = input("Enter new date in mm/dd/yyyy format: ")
        try:
            record.budget_item_date = datetime.datetime.strptime(
                date_update_input, date_format)
            record.save()
            print("Record has been updated!")
        except ValueError:
            print("Not a valid date. Please try again.")

    if column_choice == "item":
        item_update_input = input("Enter new item name: ")
        try:
            record.item_name = item_update_input.upper()
            record.save()
            print("Record has been updated!")
        except ValueError:
            print("Not a valid input. Please try again.")

    if column_choice == "amount":
        amount_update_input = input("Enter new amount in $$.$$ format: ")
        try:
            record.amount = amount_update_input
            record.save()
            print("Record has been updated!")
        except ValueError:
            print("Not a valid input. Please try again.")

    if column_choice == "category":
        for key, value in expense_categories.items():
            print(f'{key}) {value}')
        category_update_choice = input("Enter new category: ")

        if category_update_choice in expense_categories:
            try:
                record.category = expense_categories[category_update_choice]
                record.save()
                print("Record has been updated!")
            except ValueError:
                print("Not a valid input. Please try again.")


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
        # Choose a category
        for key, value in expense_categories.items():
            print(f'{key}) {value}')
        category_choice = input(
            "Choose an Expense category or Enter 'q' to quit. ").strip()
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
            f"The following record has been entered: \n Item: {item_name}\n amount: ${amount} \n Date:{budget_item_date} \n category={category} Type: {value_type}")

        save_choice = input("Would you like to save? [y/n]: ")
        if save_choice.lower() != 'n':
            Entry.create(budget_item_date=budget_item_date, item_name=item_name,
                         amount=amount, category=category, value_type=value_type)
            print("Record Saved!")
        else:
            print("Record not saved")

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
        # Choose a category
        for key, value in income_categories.items():
            print(f'{key}) {value}')
        category_choice = input("Choose an Income category: ").strip()

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
            f"The following record has been entered: \n Item: {item_name}\n amount: ${amount} \n Date:{budget_item_date} \n category: {category} Type: {value_type}")

        save_choice = input("Would you like to save? [y/n]: ")
        if save_choice.lower() != 'n':
            Entry.create(budget_item_date=budget_item_date, item_name=item_name,
                         amount=amount, category=category, value_type=value_type)
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
