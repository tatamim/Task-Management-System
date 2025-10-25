import sqlite3
from db_setup import DatabaseSetup
from database import DatabaseManager
from datetime import datetime

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def add_task(db):
    task_type = input("Enter task type (Personal/Work): ").strip().capitalize()
    if task_type not in ['Personal', 'Work']:
        print("Invalid type. Must be Personal or Work.")
        return
    user_name = input("Enter user name for the task: ").strip()
    title = input("Enter task title: ").strip()
    description = input("Enter task description (optional): ").strip()
    priority = input("Enter priority (Low/Medium/High): ").strip().capitalize()
    if priority not in ['Low', 'Medium', 'High']:
        print("Invalid priority. Must be Low, Medium, or High.")
        return
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    if not is_valid_date(due_date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    if not title or not user_name:
        print("Title and user name cannot be empty.")
        return
    try:
        task_id = db.add_task(task_type, title, description, priority, due_date, user_name)
        if task_id:
            print(f"{task_type} task '{title}' added successfully with ID {task_id}.")
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")

def delete_task(db):
    user_name = input("Enter user name for the task: ").strip()
    tasks = db.get_all_tasks(user_name)
    if not tasks:
        print("No tasks found for this user.")
        return
    print("\nTasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. ", end="")
        task.display_info()
    try:
        task_num = int(input("Select a task by number to delete: ").strip())
        if 1 <= task_num <= len(tasks):
            selected_task = tasks[task_num - 1]
            if db.delete_task(selected_task.task_id, user_name):
                print(f"Task '{selected_task.title}' deleted successfully.")
            else:
                print("Unable to delete task.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    db_setup = DatabaseSetup('tasks.db')
    db_setup.connect()
    db = DatabaseManager(db_setup.conn, db_setup.cur)
    
    while True:
        print("\nAdmin Panel Options:")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_task(db)
        elif choice == '2':
            delete_task(db)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1-3.")
    
    db_setup.close()

if __name__ == "__main__":
    main()