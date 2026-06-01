import json
from datetime import datetime

FILE_NAME = "tasks.json"

def load_tasks():
    try:
        with open(FILE_NAME, "r")as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks,file,indent=4)


def add_tasks():
    title = input("Enter Task: ")

    print("Priority options: High / Medium / Low")
    priority = input("Enter Priority: ").capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print("Invalid Priority! Setting priority to Medium. ")
        priority = "Medium"

    task = {
        "title": title,
        "priority":priority,
        "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed": False
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print("Tasks added successfully!")


def view_tasks(tasks=None):
    if tasks is None:
        tasks = load_tasks()

    if not tasks:
        print("No Tasks found.")
        return
    print("\n ===== ALL TASKS ====")

    for index, task in enumerate(tasks, start=1):
        status = "Done" if task["completed"] else "Pending"

        print(f"\nTask {index}")
        print(f"Title       : {task['title']}")
        print(f"Priority    :{task['priority']}")
        print(f"Created At  :{task['created_at']}")
        print(f"Status      :{status}")


def mark_completed():
    tasks = load_tasks()
    view_tasks(tasks)

    if not tasks:
        return
    
    try:
        task_no = int(input("Enter task number to mark as completed: "))

        if 1 <= task_no <= len(tasks):
            tasks[task_no - 1]["completed"] = True
            save_tasks(tasks)
            print("task marked as completed!")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    tasks = load_tasks()
    view_tasks(tasks)

    if not tasks:
        return
    
    try:
        tasks_no =int(input("Enter task number to delete: "))

        if 1 <= tasks_no <= len(tasks):
            delete_task = tasks.pop(tasks_no - 1)
            save_tasks(tasks)
            print(f"Deleted task: {delete_task['title']}")
        else:
            print("Invalid Task number.")
    except ValueError:
        print("Please enter a valid number.")


def filter_by_priority():
    tasks = load_tasks()

    print("Priority options: High / Medium / Low")
    priority = input("Enter priority to filter: ").capitalize()

    filtered_tasks = []

    for task in tasks:
        if task["priority"] == priority:
            filtered_tasks.append(task)

    if not filtered_tasks:
        print(f"No tasks found with {priority} priority.")
    else:
        view_tasks(filtered_tasks)


def menu():
    print("\n==== CLI TODO APP ====")
    print("1. Add New Task")
    print("2. View All Task")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. Filter by Priority")
    print("6. Exit")

while True:
    menu()

    choice= input("Enter Your Choice: ")

    if choice == "1":
        add_tasks()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_completed()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        filter_by_priority()
    elif choice == "6":
        print("Thankyou for using CLI TODO APP!")
        break
    else:
        print("Invalid choice. Please Try Again.")


