from db_setup import DatabaseSetup
from database import DatabaseManager
from models import Task
import sqlite3
from datetime import datetime


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def main():
    db_setup = DatabaseSetup('tasks.db')
    is_new_db = db_setup.connect()

    try:
        db_setup.cur.execute("SELECT 1 FROM tasks LIMIT 1")
        table_exists = True
    except sqlite3.Error:
        table_exists = False
    
    if is_new_db or not table_exists:
        print("Initializing database...")
        try:
            db_setup.setup_database('schema.sql', 'sample_data.sql')
        except Exception as e:
            print(f"Failed to set up database: {e}")
            db_setup.close()
            return
    
    db = DatabaseManager(db_setup.conn, db_setup.cur)

    while True:
        print("Wellcome to the Task Management System!")
        user_name = input("Please enter your name: ").strip()
        if not user_name:
            print("Name cannot be empty. Please try again.")
            continue

        while True:
            print("\nOptions:")
            print("1. View all tasks")
            print("2. View overdue tasks")
            print("3. Add a new task")
            print("4. Mark task as complete")
            print("5. Update task priority")
            print("6. View task history")
            print("7. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                tasks = db.get_all_tasks(user_name)
                if not tasks:
                    print("No tasks found.")
                    continue
                print("\n Your Tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}.", end="")
                    task.display_info()

            elif choice == '2':
                tasks = db.get_overdue_tasks(user_name)
                if not tasks:
                    print("No overdue tasks found.")
                    continue
                print("\nOverdue Tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. ", end="")
                    task.display_info()

            elif choice == '3':
                task_type = input("Enter task type (Personal/Work): ").strip().capitalize()
                if task_type not in ['Personal', 'Work']:
                    print("Invalid type. Must be Personal or Work.")
                    continue

                title = input("Enter task title: ").strip()
                description = input("Enter task description (optional): ").strip()

                priority = input("Enter priority (Low/Medium/High): ").strip().capitalize()
                if priority not in ['Low', 'Medium','High']:
                    print("Invalid priority. Must be Low, Medium, or High")
                    continue

                due_date = input("Enter due date (YYYY-MM-DD): ").strip()
                if not is_valid_date(due_date):
                    print("Invalid date format. Use YYYY-MM-DD.")
                    continue
                if not title:
                    print("Title cannot be empty.")
                    continue

                task_id = db.add_task(task_type, title, description, priority, due_date, user_name)
                if task_id:
                    print(f"Task '{title}' added succesfully with ID:{task_id}.")

            elif choice == '4':
                tasks = db.get_all_tasks(user_name)
                incomplete_tasks = [task for task in tasks if not task.completed]
                if not  incomplete_tasks:
                    print("No incomplete tasks to mark as complete.")
                    continue
                print("\nIncomplete Tasks:")
                for i, task in enumerate(incomplete_tasks, 1):
                    print(f"{i}. ", end="")
                    task.display_info()
                try:
                    task_num = int(input("Select a task by number to mark as complete: ").strip())
                    if 1 <= task_num <= len(incomplete_tasks):
                        selected_task = incomplete_tasks[task_num - 1]
                        if db.complete_task(selected_task.task_id, user_name):
                            print(f"Task '{selected_task.title}' marked as complete.")
                        else:
                            print("Unable to mark task as complete.")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == '5':
                tasks = db.get_all_tasks(user_name)
                if not tasks:
                    print("No tasks found.")
                    continue
                print("\nYour Tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. ", end="")
                    task.display_info()
                try:
                    task_num = int(input("Select a task by number to update priority: ").strip())
                    if 1 <= task_num <= len(tasks):
                        selected_task = tasks[task_num - 1]
                        priority = input("Enter new priority (Low/Medium/High): ").strip().capitalize()
                        if priority not in ['Low', 'Medium', 'High']:
                            print("Invalid priority. Must be Low, Medium, or High.")
                            continue
                        if db.update_task_priority(selected_task.task_id, user_name, priority):
                            print(f"Priority for task '{selected_task.title}' updated to {priority}.")
                        else:
                            print("Unable to update task priority.")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == '6':
                history = db.get_task_history(user_name)
                if not history:
                    print("No task history found.")
                    continue
                print("\nYour Task History:")
                tasks = db.get_all_tasks(user_name)
                for record in history:
                    task = next((t for t in tasks if t.task_id == record.task_id), None)
                    if task:
                        task.display_info()
                        print(f"  Action: {record.action}, Date: {record.action_date}")

            elif choice == '7':
                break
            else:
                print("Invalid choice. Please enter 1-7.")

        another = input("Do you want to start over? (yes/no): ").strip().lower()
        if another not in ['yes', 'y']:
            break

    db_setup.close()

if __name__ == "__main__":
    main()




