# Project Title: Easy Budget Application

---

> Author: Amah Martin
> Created: 9-2-2020
> Last Updated: 10-5-2020

## Table of Contents

- Project Summary
- Technical Summary
- Features
- Milestones
- Requirements to Run the Application

## Project Summary

This is a budget application that allows users to enter expenses, savings and view data visualizations of the data.

## Technical Summary

The following technologies are used to build this application:

- Python3
- sqlite

The following modules are used to run this application:

- collections
- datetime
- os
- sys
- [peewee](https://docs.peewee-orm.com/en/latest/index.html)

## Features

- Core Features will include the following\:

  1. User will have the ability to enter expenses and income information including date, cost and item and save it in a database
  2. User will have the ability to view list of expenses and income records in table format
  3. User will have the ability to view expenses and savings in chart and graph format

- The following requirements are completed for this program:

  1. Implement a “master loop” console application where the user can repeatedly enter commands/perform actions, including choosing to exit the program
  2. Create a dictionary or list, populate it with several values, retrieve at least one value, and use it in your program
  3. Create a class, then create at least one object of that class and populate it with data (see view_records and edit_record methods for example)
  4. Create and call at least 3 functions, at least one of which must return a value that is used
  5. Read data from an external file, such as text, JSON, CSV, etc (sqlite database) and use that data in your application
  6. Visualize data in a graph, chart, or other visual representation of data
  7. Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, analyze that data in some manner, and display a new result to a graph, chart, or other display

## Milestones

1. Create functions needed to add, remove, and edit expenses and income entries (Week 7)
2. Create summary information based on expenses and income such as total expenses for the month or income remaining for the month (Week 8)
3. Develop chart and graphs functionality (Week 9)
4. Create basic user interface using tkinter module (Week 10)

## Requirements to Run Application

- Ensure you have python3 program downloaded first
- Make a pull request or download the files from the GitHub repository
- In terminal navigate to root folder of easy-budget project
- In terminal type: `pip install -r requirements.txt` and push enter to download appropriate modules to run program
- Once packages are downloaded, in terminal type: `python easy_budget.py` and push enter to run the program
