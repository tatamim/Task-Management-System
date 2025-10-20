import sqlite3
import os 

class DatabaseSetup:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            # # True if new database
            is_new_db = not os.path.exists(self.db_name)
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
            self.cur.execute("PRAGMA foreign_keys = ON;") # Enable foreign key support
            return is_new_db
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    
    def _execute_sql_file(self, filename):
        try:
            with open(filename, 'r') as f:
                sql_script = f.read()
            self.cur.executescript(sql_script)
            self.conn.commit()
            print(f"Successfully execute SQL from {filename}")
        except FileNotFoundError:
            print(f"Error: SQL file not found: {filename}.")
        except sqlite3.Error as e:
            print(f"Error executing SQL from {filename}: {e}")
            self.conn.rollback()
    
    def setup_database(self, schema_file, data_file):
        print("Setting up database schema...")
        self._execute_sql_file(schema_file)
        print("Populating initial data...")
        self._execute_sql_file(data_file)