CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK (type IN ('Personal', 'Work')),
    title TEXT NOT NULL, 
    description TEXT, 
    priority TEXT NOT NULL CHECK  (priority IN ('Low', 'Medium', 'High')),
    due_date TEXT NOT NULL,
    completed INTEGER NOT NULL CHECK (completed IN (0, 1)),
    user_name TEXT NOT NULL
);

CREATE TABLE task_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    task_id INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('Created', 'Completed', 'Updated Priority')),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);