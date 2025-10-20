import sqlite3
from models import Task, PersonalTask, WorkTask, TaskRecord
from datetime import datetime

class DatabaseManager:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def get_all_tasks(self, user_name):
        try:
            self.cur.execute("SELECT task_id, type, title, description, priority, due_date, completed FROM tasks WHERE user_name = ?", (user_name,))
            rows = self.cur.fetchall()
            tasks = []
            for row in rows:
                if row[1] == 'Personal':
                    tasks.append(PersonalTask(row[0], row[2], row[3], row[4], row[5], row[6], user_name))
                elif row[1] == 'Work':
                    tasks.append(WorkTask(row[0], row[2]), row[3], row[4], row[5], row[6], user_name)
            return tasks
        except sqlite3.Error as e:
            print(f"Error fetching tasks: {e}")
            return []
    
    def get_overdue_tasks(self,user_name):
        try:
            current_date = datetime.now() .strftime("%Y-%m-%d")
            self.cur.execute("SELECT tast_id, type, title, description, priority, due_date, completed FROM tasks WHERE user_name = ? AND due_date < ? completed = 0",(user_name, current_date))
            rows = self.cur.fetchall()
            tasks = []
            for row in rows:
                if row[1] == 'Personal':
                    tasks.append(PersonalTask(row[0], row[2], row[3], row[4], row[5], row[6], user_name))
                elif row[1] == 'Work':
                    tasks.append(WorkTask(row[0], row[2], row[3], row[4], row[5], row[6], user_name))
            return tasks
        except sqlite3.Error as e:
            print(f"Error fetching overdue tasks: {e}")
            return []
    
    def add_task(self, task_type, title, description, priority, due_date, user_name):
        try:
            self.cur.execute("INSERT INTO tasks (type, title, description, priority, due_date, completed, user_name) VALUES (?, ?, ?, ?, ?, 0, ?)", (task_type, title, description, priority, due_date, user_name))
            task_id = self.cur.lastrowid
            self.cur.execute("INSERT INTO task_records (user_name, task_id, action) VALUES (?, ?, 'Created')",(user_name, task_id))
            self.conn.commit()
            return task_id
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
            self.conn.rollback()
            return None

    def complete_task(self, task_id, user_name):
        try:
            self.cur.execute("SELECT completed FROM tasks WHERE task_id = ? AND user_name = ?", (task_id, user_name))
            result = self.cur.fetchone()
            if not result or result[0] == 1:
                return False
            self.cur.execute("UPDATE tasks SET completed = 1 WHERE task_id = ?", (task_id,))
            self.cur.execute("INSERT INTO task_records (user_name, task_id, action) VALUES (?, ?, 'Completed')", (user_name, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error completing task: {e}")
            self.conn.rollback()
            return False

    def update_task_priority(self, task_id, user_name, priority):
        try:
            self.cur.execute("SELECT completed FROM tasks WHERE task_id = ? AND user_name = ?", (task_id, user_name))
            result = self.cur.fetchone()
            if not result:
                return False
            self.cur.execute("UPDATE tasks SET priority = ? WHERE task_id = ?", (priority, task_id))
            self.cur.execute("INSERT INTO task_records (user_name, task_id, action) VALUES (?, ?, 'Updated Priority')", (user_name, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating task priority: {e}")
            self.conn.rollback()
            return False

    def delete_task(self, task_id, user_name):
        try:
            self.cur.execute("SELECT task_id FROM tasks WHERE task_id = ? AND user_name = ?", (task_id, user_name))
            if not self.cur.fetchone():
                return False
            self.cur.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            self.conn.rollback()
            return False

    def get_task_history(self, user_name):
        try:
            self.cur.execute("SELECT record_id, task_id, action, action_date FROM task_records WHERE user_name = ?", (user_name,))
            rows = self.cur.fetchall()
            return [TaskRecord(row[0], user_name, row[1], row[2], row[3]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching task history: {e}")
            return []