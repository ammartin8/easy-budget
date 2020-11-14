# python packages
from collections import OrderedDict  # keeps list of options in order we want
from prettytable import PrettyTable, from_db_cursor
import datetime
import os
import sys
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

# Third-party packages
from peewee import *

db = SqliteDatabase('budgetdata.db')


class BaseModel(Model):
    class Meta:
        database = db


class Records(BaseModel):
    id = AutoField()
    Timestamp = DateTimeField(default=datetime.datetime.now)
    budget_item_date = DateField(
        default=datetime.datetime.now().date(), verbose_name="date")
    value_type = CharField(default=None)
    item_name = CharField()
    amount = DecimalField(decimal_places=2, auto_round=True)
    category = CharField(default="None")
    budget_item_month = DateField(
        default=datetime.date.today().month)
    budget_item_year = DateField(
        default=datetime.date.today().year)


def initialize():
    """Create a new database if it doesn't exist"""
    db.connect()
    db.create_tables([BaseModel], safe=True)
    db.create_tables([Records], safe=True)


def clear_cli():
    pass


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
    """Add New Record"""
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
            budget_item_month = budget_item_date.month
            budget_item_year = budget_item_date.year
        except ValueError:
            print("That's not a valid date. Please try again.")
            continue

        try:  # test negative values
            amount = "%.2f" % float(
                input("Enter cost amount in $$.$$ format "))
        except ValueError:
            print("That's not a valid cost. Please try again.")
            continue

        item_name = input("Enter item name: ").upper()
        print(
            """The following record has been entered:
            \n Item: {}
            \n Amount: ${}
            \n Date:{}
            \n Category: {}
            \n Type: {}""".format(item_name, amount, budget_item_date, category, value_type))

        while True:
            save_choice = input("Would you like to save? [y/n]: ")
            if save_choice.lower() == 'y':
                Records.create(budget_item_date=budget_item_date, item_name=item_name,
                               amount=amount, category=category, value_type=value_type,
                               budget_item_month=budget_item_month, budget_item_year=budget_item_year)
                print("Record Saved!")
                break
            elif save_choice.lower() == 'n':
                print("Record not saved")
                break
            elif save_choice.lower() != 'y' or save_choice.lower() != 'n':
                print("Not a valid choice. Please try again.")
                continue

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
        if income_date.lower() == 'q':
            break

        try:
            budget_item_date = datetime.datetime.strptime(
                income_date, date_format)
            budget_item_month = budget_item_date.month
            budget_item_year = budget_item_date.year
        except ValueError:
            print("That's not a valid date. Please try again.")
            continue

        try:
            amount = "%.2f" % float(
                input("Enter cost amount in $$.$$ format "))
        except ValueError:
            print("That's not a valid amount. Please try again.")
            continue

        item_name = input("Enter item name: ").upper()
        print(
            """The following record has been entered:
            \n Item: {}
            \n amount: ${}
            \n Date:{}
            \n Category: {}
            \n Type: {}
            """.format(item_name, amount, budget_item_date, category, value_type))

        while True:
            save_choice = input("Would you like to save? [y/n]: ")
            if save_choice.lower() == 'y':
                Records.create(budget_item_date=budget_item_date, item_name=item_name,
                               amount=amount, category=category, value_type=value_type,
                               budget_item_month=budget_item_month, budget_item_year=budget_item_year)
                print("Record Saved!")
                break
            elif save_choice.lower() == 'n':
                print("Record not saved")
                break
            elif save_choice.lower() != 'y' or save_choice.lower() != 'n':
                print("Not a valid choice. Please try again.")
                continue

        cont_choice = input("Would you like to add another item? [y/n] ")
        if cont_choice.lower() == 'y':
            continue
        elif cont_choice.lower() == 'n':
            break


def view_records():
    """View List of Budget Items"""
    table_view = Records
    cursor = db.execute_sql(
        """SELECT id as ID
        , strftime("%m-%d-%Y",budget_item_date) as Date
        , item_name as Item
        , amount as Amount
        , category as Category
        , value_type as Type
        , budget_item_month as Month
        , budget_item_year as Year
        FROM Records
        """)

    # from_db_cursor creates the pretty table using results from cursor object and saves to myTable
    myTable = from_db_cursor(cursor)
    print(myTable)

    rec_choice = input(
        "Select a number if you want to view a specific record. Enter q to quit to main menu: ")

    while rec_choice.lower() != 'q':
        try:
            if rec_choice.lower() in table_view.id:
                record = table_view.get(table_view.id == rec_choice)
                print(f"id: {record.id}")
                print(f"Date: {record.budget_item_date.strftime('%m-%d-%Y')}")
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
            return print("Not a valid option. Please try again.")


def edit_record(record):
    """Edit A Record"""
    date_format = '%m/%d/%Y'

    print(f"1) Date: {record.budget_item_date.strftime('%m-%d-%Y')}")
    print(f"2) Item: {record.item_name}")
    print(f"3) Amount: {record.amount}")
    print(f"4) Category: {record.category}")
    print(f"5) Type: {record.value_type} \n\n")

    column_choice = input(
        "What field do you want to edit? Select a number: ")

    if column_choice == "1":
        date_update_input = input("Enter new date in mm/dd/yyyy format: ")
        try:
            record.budget_item_date = datetime.datetime.strptime(
                date_update_input, date_format)
            record.budget_item_month = record.budget_item_date.month
            record.budget_item_year = record.budget_item_date.year
            record.save()
            print("Record has been updated!")
        except ValueError:
            return print("Not a valid date. Please try again.")

    if column_choice == "2":
        item_update_input = input("Enter new item name: ")
        try:
            record.item_name = item_update_input.upper()
            record.save()
            print("Record has been updated!")
        except ValueError:
            print("Not a valid input. Please try again.")

    if column_choice == "3":
        amount_update_input = input("Enter new amount in $$.$$ format: ")
        try:
            record.amount = amount_update_input
            record.save()
            print("Record has been updated!")
        except ValueError:
            print("Not a valid input. Please try again.")

    if column_choice == "4":
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


def summary_report():
    """View Summary Report"""
    # TODO: Select available month and year to view

    # Show total Expenses for the month
    total_expenses = Records.select(
        fn.Sum(Records.amount).alias('Total Expenses')).where(Records.value_type == "expense").scalar()
    if total_expenses == None:  # potential use case for dunder str method to re-write None to 0
        total_expenses = "0"
    print("Total amount of expenses spent: ${}".format(
        "%.2f" % float(total_expenses)))

    # Show total Income for the month
    total_income = Records.select(
        fn.Sum(Records.amount).alias('Total Income')).where(Records.value_type == "income").scalar()
    if total_income == None:
        total_income = "0"
    print("Total amount of income earned: ${}".format(
        "%.2f" % float(total_income)))

    # Show the remaining balance for the month
    remaining_balance = float(total_income) - float(total_expenses)
    print("Your remaining balance: ${}".format(
        "%.2f" % float(remaining_balance)))


# Pandas Analysis
def run_pandas():
    """View Pandas Dataframe (Testing)"""
    # Saving sqlite database query to pandas dataframe
    df = pd.read_sql_query("SELECT * FROM Records", db)

    # Creating a Filter to show Expenses Breakdown Only
    exp_filt = df['value_type'] == 'expense'

    # Create a groups for category and value_type
    exp_grp = df.loc[exp_filt].groupby(['category'])
    value_type_grp = df.groupby(['value_type'])

    # Sum values by category for expenses only
    exp_cat_totals = exp_grp['amount'].sum()

    # Save total expenses and income as series for barchart
    exp_inc_tot = value_type_grp['amount'].sum()
    exp_inc_labels = exp_inc_tot.keys()
    colors = ['#8E2F5C', '#749D34']

    # Combining Both Plots by Subplotting
    plt.style.use('fivethirtyeight')

    fig, (ax1) = plt.subplots(nrows = 1, ncols=1)
    fig, (ax2) = plt.subplots(nrows = 1, ncols=1)

    # Bar Chart Summary
    ax1.set_title("Overall Summary for Expenses and Income", fontsize=15)
    ax1.set_ylabel('Total Amount ($)')

    ax1.bar(exp_inc_labels, exp_inc_tot, color=colors)

    # Pie Chart Expense Breakdown Summary
    ax2.set_title("Expenses Breakdown", fontsize=15)
    slices = exp_cat_totals
    labels = exp_cat_totals.keys()
    x =.08
    explode = [x,x,x,x,x,x]

    ax2.pie(slices, labels=labels, autopct='%1.1f%%', pctdistance=.78, explode=explode)

    #draw circle in middle of Pie chart for Dounut Style Chart
    centre_circle = plt.Circle((0,0),0.60,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)



    plt.tight_layout()
    plt.axis('equal')
    plt.show()


menu = OrderedDict([
    ('1', add_record),
    ('2', view_records),
    ('3', summary_report),
    ('4', run_pandas),
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
