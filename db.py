import sqlite3
import pandas as pd


# Initial creation the database with the tables habit and habit_task
def create_db(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        habit_name TEXT PRIMARY KEY,
        period TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS habit_task (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT,
        created TEXT,
        due TEXT,
        status TEXT,
        streak_counter INTEGER)""")
    db.commit()


# Connect to database
def get_db(name="database.db"):
    db = sqlite3.connect(name)
    create_db(db)
    return db


# Insert a new habit in the table habit
def insert_habit(selected_habit, selected_period, db):
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO habit (habit_name, period) VALUES (?, ?)",
                    (selected_habit, selected_period))
        db.commit()
    except sqlite3.IntegrityError:
        print("You have already chosen this habit. Please try another one")
        exit()


# Insert a new task in the table habit_task
def insert_task(habit_name, created, due, status, streak_counter, db):
    cur = db.cursor()
    cur.execute("INSERT INTO habit_task "
                "(habit_name, created, due, status, streak_counter)"
                "VALUES (?, ?, ?, ?, ?)",
                (habit_name, created, due, status, streak_counter))
    db.commit()


# Update the status of a specific task
def update_task(task_id, status, db):
    cur = db.cursor()
    cur.execute("UPDATE habit_task SET status = ? WHERE task_id = ?",
                (status, task_id,))
    db.commit()


# Return all tasks
def return_all_tasks(db):
    task_list = pd.read_sql_query("SELECT * FROM habit_task;", db)
    task_list["created"] = pd.to_datetime(task_list["created"])
    task_list["due"] = pd.to_datetime(task_list["due"])
    return task_list


# Return only open tasks
def return_open_task(db):
    task_list = pd.read_sql_query("SELECT * FROM habit_task WHERE status = 'open'", db)
    task_list["created"] = pd.to_datetime(task_list["created"])
    task_list["due"] = pd.to_datetime(task_list["due"])
    return task_list


# Return all habits
def return_habit(db):
    current_habits = pd.read_sql_query("SELECT * FROM habit", db)
    return current_habits


# Delete habit including its tasks from habit table and habit_task table
def delete_task(selected_habit, db):
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE habit_name = ?",
                (selected_habit,))
    db.commit()
    cur.execute("DELETE FROM habit_task WHERE habit_name = ?",
                (selected_habit,))
    db.commit()
    db.close()
