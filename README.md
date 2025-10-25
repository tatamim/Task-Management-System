Python & SQL Command-Line Task Management System
Overview
This is a command-line application that allows users to manage tasks (personal or work) using Python 3 and SQLite. Users can add, prioritize, complete, delete, and view tasks (including overdue ones). The project demonstrates all pillars of Object-Oriented Programming (OOP):

Encapsulation: Data and methods are bundled in classes (e.g., Task encapsulates title, priority, etc.).
Abstraction: Abstract base class (Task) hides implementation details and provides a blueprint.
Inheritance: Subclasses like PersonalTask and WorkTask inherit from Task.
Polymorphism: Subclasses override methods (e.g., display_info()) for specific behavior.

Setup Instructions
Prerequisites:

Python 3.x installed on your system.
No additional server setup is required for SQLite as it is built into Python.

Project Structure:

main.py: Entry point for users to manage tasks.
admin.py: For admins to add or delete tasks.
database.py: Manages database queries and operations.
db_setup.py: Handles database connection and schema setup.
models.py: Defines Task, PersonalTask, WorkTask, and TaskRecord classes.
schema.sql: Defines the database schema.
sample_data.sql: Populates the database with sample tasks.

Installation:

Ensure all files are in the same directory.
No external dependencies are required beyond Python's standard library.

Initialize the Database:

Run python main.py for the first time. The application will create tasks.db and populate it with tables and sample data from schema.sql and sample_data.sql.

Running the Application:

For users: Execute python main.py to create, complete, prioritize, or view tasks.
For admins: Execute python admin.py to add or delete tasks.

Usage
In main.py:

Enter your name.
Choose options: 
View all tasks
View overdue tasks
Add a new task
Mark task as complete
Update task priority
View your task history
Exit


Select tasks by number where applicable.

In admin.py:

Add new tasks (personal or work) or delete tasks.

Notes

The database (tasks.db) is created automatically if it doesn't exist.
Ensure schema.sql and sample_data.sql are in the same directory as main.py.
Task priorities are Low, Medium, or High; due dates are stored in YYYY-MM-DD format.

Bonus Features

View overdue tasks based on due date and current date.
Update task priority.
View task history for a user.
Basic error handling for invalid inputs (e.g., non-numeric choices, invalid dates).

Contributing
This is a student project demonstrating OOP pillars. For enhancements, contact the developer.