from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, task_id, title, description, priority, due_date, completed, user_name):
        self._task_id = task_id
        self._title = title
        self._description = description
        self._priority = priority
        self._due_date = due_date
        self._completed = completed
        self._user_name = user_name

    # Encapsulation: Properties for controlled access to attributes
    @property
    def task_id(self):
        return self._task_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description
    
    @property
    def priority(self):
        return self._priority
    
    @property
    def due_date(self):
        return self._due_date
    
    @property
    def completed(self):
        return self._completed
    
    @property
    def user_name(self):
        return self._user_name
    
    # Abstraction: Abstract method to enforce a blueprint for subclasses
    @abstractmethod
    def display_info(self):
        """Display task information - overriden subclass."""
        pass

# Inheritance: PersonalTask inherits from task
class PersonalTask(Task):
    def display_info(self):
        # Polymorphism: Overrides display_info for personal tasks
        print(f"Personal Task: {self.title} - {self.description} (Priority: {self.priority}, Due: {self.due_date}, Completed: {'Yes' if self.completed else 'No'})")

# Inheritance: WorkTask inherits from Task
class WorkTask(Task):
    def display_info(self):
        print(f"Personal Task: {self.title} - {self.description} (Priority: {self.priority}, Due: {self.due_date}, Completed: {'Yes' if self.completed else 'No'})")

class TaskRecord:
    def __init__(self, record_id, user_name, task_id, action, action_date):
        self.record_id = record_id
        self.user_name = user_name
        self.task_id = task_id
        self.action = action
        self.action_date = action_date