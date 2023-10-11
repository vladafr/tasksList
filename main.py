from datetime import datetime
from tabulate import tabulate
import tkinter as tk
import json

current_datetime = datetime.now()
current_date = current_datetime.strftime("%d-%m-%Y")


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks_list = json.load(file)
    except FileNotFoundError:
        tasks_list = []
        with open("tasks.json", "w") as file:
            json.dump(tasks, file)
    return tasks_list


tasks = load_tasks()


def save_tasks():
    with open("tasks.json", 'w') as file:
        json.dump(tasks, file, indent=4)


def add_task(description):
    last_task_id = 1
    if len(tasks) > 0:
        last_task_id = tasks[-1]["id"] + 1
    new_task = {
        "id": last_task_id,
        "description": description,
        "status": "Incomplete",
        "date": current_date
    }
    tasks.append(new_task)
    save_tasks()
    print("Task successfully added.")


def remove_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            print(f"Task number {task_id} was successfully removed.")
            save_tasks()
            return
        else:
            print("The specified ID was not found.")


def mark_as_complete(task_id):
    for task in tasks:
        if task["id"] == task_id and task["status"] != "Complete":
            task["status"] = "Complete"
            print(f"Task number {task_id} was successfully marked as complete!")
            save_tasks()
            return
        else:
            print("The task is already marked as complete.")


def print_incomplete_tasks():
    for task in tasks:
        if task["status"] == "Incomplete":
            print(task)
        else:
            print("You have no tasks!")


def edit_task(task_id, description):
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            save_tasks()
        else:
            print(f"The task number {task_id} does not exist.")


def remove_tasks():
    tasks.clear()
    save_tasks()
    print("All tasks have been removed.")


def cli(short_text=True):
    text = ("What would you like to do?\n1 - View tasks\n2 - Add a task\n3 - Remove a task\n"
            "4 - Edit a task\n5 - Mark a task as complete\n"
            "6 - Remove all tasks\n7 - View incomplete tasks\n8 - Exit\nType: ")
    if not short_text:
        text = "Would you like to perform another action?: "
    options = input(text)
    match options:
        case '1':
            print(tabulate(tasks))
        case '2':
            description = input("Enter description: ")
            add_task(description)
        case '3':
            task_id = input("Enter ID: ")
            remove_task(task_id)
        case '4':
            task_id = input("Enter ID: ")
            new_description = input("Enter new description: ")
            edit_task(task_id, new_description)
        case '5':
            task_id = input("Enter ID: ")
            mark_as_complete(task_id)
        case '6':
            remove_tasks()
        case '7':
            print_incomplete_tasks()
        case '8':
            exit()
    cli(False)


# GUI -------------------

root = tk.Tk()
root.title("Tasks List")
root.geometry("800x500")

# Creating the welcome text label at the top of the interface
welcome_label = tk.Label(root, text="Welcome to Tasks List", font=("Arial", 24, "bold"))
welcome_label.pack(pady=30)


# Creating functions to load tasks, then to show them in the frame
def load_tasks_ui():
    try:
        with open("tasks.json", "r") as file:
            tasks_ui = json.load(file)
            return tasks_ui
    except FileNotFoundError:
        return []


def show_tasks_ui():
    tasks_ui = load_tasks_ui()

    if tasks_ui:
        task_text = "\n".join([f"{task['id']}. {task['description']} ({task['status']}) - {task['date']}" for task in tasks_ui])
    else:
        task_text = "No tasks available."

    task_display.config(text=task_text)


# Creating the load button, which is connected to the show_tasks_ui function
load_button = tk.Button(root, text="Load Tasks", command=show_tasks_ui)
load_button.pack(pady=10)

# Creating a frame for displaying current tasks
frame = tk.Frame(root, bg="lightgray", padx=20, pady=20)
frame.pack(fill="both", expand=True)

task_display = tk.Label(
    frame,
    text="",
    font=("Times New Roman", 14),
)
task_display.pack(fill="both", expand=True)

# Creating the add task button, along with the necessary functions, such as add_task_clicked, 'Add' button and so on
entry = None
add = None
done = None
frame_add = None


# ADD TASK BUTTON
def add_task_btn():
    global entry, add, done, frame_add
    entry = tk.Entry(root, font=("Arial", 16))
    entry.pack(pady=20)
    frame_add = tk.Frame(root)
    frame_add.pack(padx=20, pady=20)
    add = tk.Button(frame_add, text="Add", command=lambda: add_task_clicked(entry.get()))
    add.grid(row=0, column=0, padx=10)
    done = tk.Button(frame_add, text="✓", command=done_add)
    done.grid(row=0, column=1, padx=10)
    add_button.config(state=tk.DISABLED)


def add_task_clicked(description):
    add_task(description)
    save_tasks()
    show_tasks_ui()


def done_add():
    entry.pack_forget()
    add.grid_forget()
    done.grid_forget()
    add_button.config(state=tk.NORMAL)
    frame_add.pack_forget()


def remove_all_btn():
    remove_tasks()
    save_tasks()
    show_tasks_ui()


def exit_btn():
    root.destroy()
    exit()


remove_entry = None
remove = None
done_rmv = None
frame_remove = None


def remove_btn():
    global remove_entry, remove, done_rmv, frame_remove
    remove_entry = tk.Entry(root, font=("Arial", 16))
    remove_entry.pack(pady=20)
    frame_remove = tk.Frame(root)
    frame_remove.pack(padx=20, pady=20)
    remove = tk.Button(frame_remove, text="Remove", command=lambda: remove_task_clicked(remove_entry.get()))
    remove.grid(row=0, column=0, padx=10)
    done_rmv = tk.Button(frame_remove, text="✓", command=done_remove)
    done_rmv.grid(row=0, column=1, padx=10)
    remove_button.config(state=tk.DISABLED)


def remove_task_clicked(task_id):
    remove_task(task_id)
    save_tasks()
    show_tasks_ui()


def done_remove():
    remove_entry.pack_forget()
    frame_remove.pack_forget()
    remove.grid_forget()
    done_rmv.grid_forget()
    remove_button.config(state=tk.NORMAL)


# Creating the frame along with all the buttons needed for the interface
frame_buttons = tk.Frame(root)
frame_buttons.pack(padx=20, pady=20)
add_button = tk.Button(frame_buttons, text="Add task", command=add_task_btn)
add_button.grid(row=0, column=0, padx=10)

edit_button = tk.Button(frame_buttons, text="Edit task", command=None)
edit_button.grid(row=0, column=1, padx=10)

remove_button = tk.Button(frame_buttons, text="Remove task", command=remove_btn)
remove_button.grid(row=0, column=2, padx=10)

removeAll_button = tk.Button(frame_buttons, text="Remove all tasks", command=remove_all_btn)
removeAll_button.grid(row=0, column=3, padx=10)

exit_button = tk.Button(frame_buttons, text="Exit", command=exit_btn)
exit_button.grid(row=0, column=4, padx=10)

# Setting up the icon
root.iconbitmap("checklist.ico")

root.mainloop()
