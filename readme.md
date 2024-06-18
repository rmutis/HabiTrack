# Habi Track Documentation
Welcome to the documentation of Habi Track. 
The following chapters will explain to you 
the aim of this application as well how to install 
and use it.

## What is Habi Track?
Habi Track is a habit tracker application that helps 
you implementing new, desirable habits as a routine. 
The application has following main features: 
- Select a habit from a pre-defined list or create new ones
- Select the frequency how often the habit shall be checked
- Automatic creation of a habit task including due date 
- Complete the habit tasks before the due date
- Get a reminder of your current tasks
- Analyse how good you stick to your habits, 
e.g. the run streak shows you how often you completed
habit tasks in a row

## Installation
The solution was programmed with Python 3.12 using 
PyCharm Community Edition 2023.3.6 on a Windows notebook.
The minimum requirement for using the application is 
installation of Python 3.12.

Download all files in a dedicated directory and open a 
terminal window there. The following command will install
all relevant packages for using Habi Track:
```
pip install -r requirements.txt
```

## How to start Habi Track
Open a terminal window in the directory of Habi Track
and run following command to start 
the main menu:
```
python main.py
```
In the main menu you will find following options:

- *Select pre-defined habit*: You can choose from following
habits: Sport, Sleep sufficient, Eat healthy, Meditation,
Cold shower
- *Create new habit*
- *Complete habit task*: check off a habit task
- *Remind of current habits*: Shows all current open habit
tasks including due date
- *Analyze habits*: Following options are available
  
  - *Return list of all currently tracked habits*
  - *Return list of all habits with the same periodicity*
  - *Return the longest run streak of all habits*
  - *Return the longest run streak of a selected habits*
  - *Return percentage of completed habits*: This function 
  calculates the percentage of successful completed tasks 
  for a habit compared to the complete amount of habit tasks
- *Delete habit*: This will delete a habit and all its 
related information permanently from the database.
- *Exit*: Leave the application without using any option  

Some additional information concerning the usage of 
Habi Track:
- The defined habits are also marked as key in the 
habit-table: i.e. you cannot use two habits with the
same name. This should help to avoid any confusion.
- When starting the application all open habit tasks are
checked if in any of them the due date is exceeded. If so 
the habit task is marked as missed and a successor task
is created.

## How to perform automatic unit tests
The application contains automatic unit tests using Pytest.
The unit test contain data of two habits from 1st of April 
2024 until 1st of May 2024.
The aim of these unit tests is to ensure correct functionality
of the core functions of Habi Track:
- Creating new habits
- Correct calculation of due date, streak counter, status
and table entries
- Correct analysis of the created data
- Deletion of a habit
All these tests will be performed on a dedicated database
called test.db. This database is created at the beginning 
of the tests and deleted at the end.

Open a terminal window in the directory of Habi Track
and run following command to run the unit tests:
```
pytest .
```