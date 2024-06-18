import questionary
from datetime import datetime, timedelta
from habit import Habit, Task
from analysis import run_streak, run_streak_one_habit, percent_calc
from db import return_open_task, update_task, delete_task, return_habit, get_db


# cli-Function is used for basic navigation within the solution
def cli():
    db = get_db()
    overdue_tasks(db)
    choice = questionary.select(
        "Welcome to Habi Track! Please select an option:",
        choices=["Select pre-defined habit",
                 "Create new habit",
                 "Complete habit task",
                 "Remind of current habits",
                 "Analyze habits",
                 "Delete habit",
                 "Exit"]
    ).ask()

    if choice == "Select pre-defined habit":
        selected_habit = questionary.select(
            "Please select a habit:",
            choices=["Sport",
                     "Sleep sufficient",
                     "Eat healthy",
                     "Meditation",
                     "Cold shower"]
        ).ask()
        # Calls function to manage adding new habit
        add_habit_and_task(selected_habit, db)

    elif choice == "Create new habit":
        new_habit = questionary.text("What is the name of the habit?").ask()
        # Calls function to manage adding new habit
        add_habit_and_task(new_habit, db)

    elif choice == "Complete habit task":
        # Call function to select a habit for completion and updating status of task
        selected_habit, task_list = select_habit(db)
        completed_task_id, new_due_date, new_counter = get_id_date_counter(task_list, selected_habit)
        update_task(completed_task_id, "completed", db)
        # Creation of habit task object and store it on the db using Task-class in habit.py
        successor_task = Task(selected_habit, new_due_date, new_counter)
        successor_task.task_store(db)
        db.close()

    elif choice == "Remind of current habits":
        # Call function to get all open tasks and print them
        task_list = return_open_task(db)
        print("Here are your current tasks:\n", task_list)

    elif choice == "Analyze habits":
        choice = questionary.select(
            "Which analysis would you like to choose?",
            choices=["Return list of all currently tracked habits",
                     "Return list of all habits with the same periodicity",
                     "Return the longest run streak of all habits",
                     "Return the longest run streak of a selected habits",
                     "Return percentage of completed habits"]
        ).ask()
        if choice == "Return list of all currently tracked habits":
            print(return_habit(db))
        if choice == "Return list of all habits with the same periodicity":
            # Call function to ask for the respective periodicity and return only habits with it
            selected_period = select_period()
            habit_hits = return_habit(db).loc[return_habit(db)["period"] == selected_period]
            print(habit_hits)
        if choice == "Return the longest run streak of all habits":
            # Call function in analysis-module to get longest run streak of all open tasks and of all tasks ever
            open_result, ever_result = run_streak(db)
            print("Here are the longest run streaks of all current open habit tasks:\n", open_result)
            print("Here are the longest run streaks ever achieved:\n", ever_result)
        if choice == "Return the longest run streak of a selected habits":
            # Call function to select a habit and return longest run streak of this habit
            selected_habit, task_list = select_habit(db)
            open_result, ever_result = run_streak_one_habit(db, selected_habit)
            # Check if the run streak of current open habit is also the longest run streak
            if open_result.iloc[0, 5] == ever_result.iloc[0, 5]:
                print("Congratulations! Your longest run streak for ", selected_habit, " is ", open_result.iloc[0, 5],
                      ".\nThis is also your current run streak")
            else:
                print("Your longest run streak for ", selected_habit, " is ", ever_result.iloc[0, 5],
                      ".\n Your current run streak is ", open_result.iloc[0, 5])
        if choice == "Return percentage of completed habits":
            # Call function to calculate the percentage of completed habits
            habit_list = percent_calc(db)
            print("Here are your results")
            print(habit_list[["habit_name", "Percent of completed habits"]])

    elif choice == "Delete habit":
        # Call function to select a habit and afterward to delete it
        selected_habit, task_list = select_habit(db)
        delete_task(selected_habit, db)
        db.close()
        print("The habit ", selected_habit, " has been deleted successfully. Have a nice day")
    else:
        print("Exiting Habi Track. See you soon.")
    db.close()


# Function to select a habit period
def select_period():
    selected_period = questionary.select(
        "Please select an period:",
        choices=["every day", "every second day", "every third day", "every week"]
    ).ask()
    return selected_period


# Function to calculate the due date based on the selected frequency
def calc_due(period):
    if period == "every day":
        due = datetime.now() + timedelta(days=1)
    elif period == "every second day":
        due = datetime.now() + timedelta(days=2)
    elif period == "every third day":
        due = datetime.now() + timedelta(days=3)
    else:
        due = datetime.now() + timedelta(days=7)
    return due


# Function to get the task id to be completed and to calculate new due date and streak counter
# for successor task
def get_id_date_counter(task_list, selected_habit):
    selected_task = task_list.loc[task_list["habit_name"] == selected_habit]
    completed_task_id = int(selected_task.iloc[0, 0])
    diff = selected_task.iloc[0, 3] - selected_task.iloc[0, 2]
    new_due_date = datetime.now() + diff
    new_counter = int(selected_task.iloc[0, 5] + 1)
    return completed_task_id, new_due_date, new_counter


# Function to ask user which habit shall be selected and return the result as well as task list
def select_habit(db):
    task_list = return_open_task(db)
    selected_habit = questionary.select(
        "Which habit shall be selected?",
        choices=sorted(task_list["habit_name"])
    ).ask()
    return selected_habit, task_list


# Function calling sub-functions for frequency selection and habit/task instantiation as well as storing
# for initially created/selected habits
def add_habit_and_task(selected_habit, db):
    selected_period = select_period()
    # Creates the habit object based on the selected habit and its frequency and
    # stores it on the db using Habit-class in habit.py
    habit_object = Habit(selected_habit, selected_period)
    habit_object.habit_store(db)
    # Usage of calc_due()-function to transform the selected habit period
    # (e.g. "every day") into datetime format.
    due_date = calc_due(selected_period)
    # Creation of habit task object and store it on the db using Task-class in habit.py
    habit_task_obj = Task(selected_habit, due_date, 0)
    habit_task_obj.task_store(db)


# Function to check for any open task with exceeded due date.
# If so tasks is marked as missed and successor task is created.
def overdue_tasks(db):
    task_list = return_open_task(db)
    length = (len(task_list))
    for x in range(0, length):
        if task_list.iloc[x, 3] < datetime.now():
            missed_task_id = int(task_list.iloc[x, 0])
            missed_habit_name = task_list.iloc[x, 1]
            diff = task_list.iloc[x, 3] - task_list.iloc[x, 2]
            new_due_date = datetime.now() + diff
            update_task(missed_task_id, "missed", db)
            successor_task = Task(missed_habit_name, new_due_date, 0)
            successor_task.task_store(db)


if __name__ == "__main__":
    cli()
