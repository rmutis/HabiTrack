from db import return_all_tasks, return_open_task, return_habit


# Return maximum value of the streak counter for all currently open tasks and all tasks ever of all habits
def run_streak(db):
    task_list = return_all_tasks(db)
    open_tasks = return_open_task(db)
    max_open = max(open_tasks["streak_counter"])
    open_result = open_tasks.loc[open_tasks["streak_counter"] == max_open]
    max_ever = max(task_list["streak_counter"])
    ever_result = task_list.loc[task_list["streak_counter"] == max_ever]
    return open_result, ever_result


# Return maximum value of the streak counter for all currently open tasks and all tasks ever of one habit
def run_streak_one_habit(db, selected_habit):
    task_list = return_all_tasks(db)
    open_tasks = return_open_task(db)
    open_tasks_habit = open_tasks.loc[open_tasks["habit_name"] == selected_habit]
    max_open = max(open_tasks_habit["streak_counter"])
    open_result = open_tasks_habit.loc[open_tasks_habit["streak_counter"] == max_open]
    task_list_habit = task_list.loc[task_list["habit_name"] == selected_habit]
    max_ever = max(task_list_habit["streak_counter"])
    ever_result = task_list_habit.loc[task_list_habit["streak_counter"] == max_ever]
    return open_result, ever_result


# Function to calculate the percentage of completed tasks
def percent_calc(db):
    task_list = return_all_tasks(db)
    habit_list = return_habit(db)
    habit_list["Percent of completed habits"] = ""
    for x in range(0, len(habit_list)):
        task_cur_hab = task_list.loc[task_list["habit_name"] == habit_list.iloc[x, 0]]
        completed = task_cur_hab[task_cur_hab["status"] == "completed"].count()
        missed = task_cur_hab[task_cur_hab["status"] == "missed"].count()
        if completed.iloc[0] == 0:
            habit_list.iloc[x, 2] = "nan"
        else:
            habit_list.iloc[x, 2] = completed.iloc[0] * 100 / (completed.iloc[0] + missed.iloc[0])
    return habit_list
