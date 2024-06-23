import os
from freezegun import freeze_time
from datetime import datetime, timedelta
from main import calc_due, get_id_date_counter, overdue_tasks
from habit import Habit, Task
from analysis import run_streak, run_streak_one_habit, percent_calc
from db import return_all_tasks, return_open_task, update_task, delete_task, return_habit, get_db, create_db


# Creation of test database and insert first two habits.
# Check if the due dates are calculated correctly and correct amount of entries in db.
@freeze_time("2024-04-01")
def test_creation():
    db = get_db("test.db")
    create_db(db)
    first_habit = Habit("Sport", "every second day")
    first_habit.habit_store(db)
    first_due = calc_due("every second day")
    assert first_due == datetime.now() + timedelta(days=2)
    first_task = Task("Sport", first_due, 0)
    first_task.task_store(db)
    second_habit = Habit("No sweets", "every third day")
    second_habit.habit_store(db)
    second_due = calc_due("every third day")
    assert second_due == datetime.now() + timedelta(days=3)
    second_task = Task("No sweets", second_due, 0)
    second_task.task_store(db)
    assert len(return_all_tasks(db)) == 2
    assert len(return_habit(db)) == 2
    db.close()


# General function to be used if habit is completed until due date
def success(habit_name):
    db = get_db("test.db")
    task_list = return_open_task(db)
    completed_task_id, new_due_date, new_counter = get_id_date_counter(task_list, habit_name)
    update_task(completed_task_id, "completed", db)
    successor_task = Task(habit_name, new_due_date, new_counter)
    successor_task.task_store(db)
    all_tasks = return_all_tasks(db)
    db.close()
    return new_due_date, new_counter, all_tasks


# General function to be used if habit is not completed until due date
def missed():
    db = get_db("test.db")
    overdue_tasks(db)
    all_tasks = return_all_tasks(db)
    db.close()
    return all_tasks


# Start of habit tracking: Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-03")
def test_success_one():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 1
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 1
    assert len(all_tasks) == 4
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2


# Missing sport habit but completing sweets habit.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-06")
def test_missed_one():
    all_tasks = missed()
    open_sport = all_tasks[(all_tasks["habit_name"] == "Sport") & (all_tasks["status"] == "open")]
    assert open_sport.iloc[0, 3] == datetime.now() + timedelta(days=2)
    assert open_sport.iloc[0, 5] == 0
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 2
    assert len(all_tasks) == 6
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 3
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 1


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-08")
def test_success_two():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 1
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 3
    assert len(all_tasks) == 8
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 5
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 1


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-10")
def test_success_three():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 2
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 4
    assert len(all_tasks) == 10
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 7
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 1


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-12")
def test_success_four():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 3
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 5
    assert len(all_tasks) == 12
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 9
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 1


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-14")
def test_success_five():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 4
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 6
    assert len(all_tasks) == 14
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 11
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 1


# Both habits are missed now.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-18")
def test_missed_two():
    all_tasks = missed()
    open_sport = all_tasks[(all_tasks["habit_name"] == "Sport") & (all_tasks["status"] == "open")]
    assert open_sport.iloc[0, 3] == datetime.now() + timedelta(days=2)
    assert open_sport.iloc[0, 5] == 0
    open_sport = all_tasks[(all_tasks["habit_name"] == "No sweets") & (all_tasks["status"] == "open")]
    assert open_sport.iloc[0, 3] == datetime.now() + timedelta(days=3)
    assert open_sport.iloc[0, 5] == 0
    assert len(all_tasks) == 16
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 11
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 3


# Missing sport habit but completing sweets habit.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-21")
def test_missed_three():
    all_tasks = missed()
    open_sport = all_tasks[(all_tasks["habit_name"] == "Sport") & (all_tasks["status"] == "open")]
    assert open_sport.iloc[0, 3] == datetime.now() + timedelta(days=2)
    assert open_sport.iloc[0, 5] == 0
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 1
    assert len(all_tasks) == 18
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 12
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 4


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-23")
def test_success_six():
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 1
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 2
    assert len(all_tasks) == 20
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 14
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 4


# Completion only of Sports.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-25")
def test_success_seven():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 2
    assert len(all_tasks) == 21
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 15
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 4


# Missing sweets but completing sport.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-27")
def test_missed_four():
    all_tasks = missed()
    open_sweets = all_tasks[(all_tasks["habit_name"] == "No sweets") & (all_tasks["status"] == "open")]
    assert open_sweets.iloc[0, 3] == datetime.now() + timedelta(days=3)
    assert open_sweets.iloc[0, 5] == 0
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 3
    assert len(all_tasks) == 23
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 16
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 5


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-04-29")
def test_success_eight():
    missed()
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 4
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 1
    assert len(all_tasks) == 25
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 18
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 5


# Completion of both habit tasks.
# Check if due dates, counter and amount of habit tasks are calculated correctly.
@freeze_time("2024-05-01")
def test_success_nine():
    sport_due_date, sport_counter, all_tasks = success("Sport")
    assert sport_due_date == datetime.now() + timedelta(days=2)
    assert sport_counter == 5
    sweets_due_date, sweets_counter, all_tasks = success("No sweets")
    assert sweets_due_date == datetime.now() + timedelta(days=3)
    assert sweets_counter == 2
    assert len(all_tasks) == 27
    assert len(all_tasks[all_tasks["status"] == "open"]) == 2
    assert len(all_tasks[all_tasks["status"] == "completed"]) == 20
    assert len(all_tasks[all_tasks["status"] == "missed"]) == 5


# Test of analysis-module based on the created data
def test_analysis():
    db = get_db("test.db")
    # Return all tracked habits
    assert len(return_habit(db)) == 2
    # Return habits with the same frequency
    selected_period = "every second day"
    habit_hits = return_habit(db).loc[return_habit(db)["period"] == selected_period]
    assert habit_hits.iloc[0, 0] == "Sport"
    # Return the longest run streak of all habits
    open_result, ever_result = run_streak(db)
    assert open_result.iloc[0, 1] == "Sport"
    assert open_result.iloc[0, 5] == 5
    assert ever_result.iloc[0, 1] == "No sweets"
    assert ever_result.iloc[0, 5] == 6
    # Return the run streak of a selected habit (No sweets)
    open_result, ever_result = run_streak_one_habit(db, "No sweets")
    assert open_result.iloc[0, 5] == 2
    assert ever_result.iloc[0, 5] == 6
    # Percentage of completed habit tasks
    habit_list = percent_calc(db)
    assert habit_list.iloc[0, 2] == 76.92307692307692
    assert habit_list.iloc[1, 2] == 83.33333333333333
    db.close()


# Test of habit deletion
def test_delete_habit():
    db = get_db("test.db")
    delete_task("Sport", db)
    db = get_db("test.db")
    current_habits = return_habit(db)
    assert current_habits.iloc[0, 0] == "No sweets"
    db.close()


# Deletion of test.db
def test_delete_db():
    os.remove("test.db")
