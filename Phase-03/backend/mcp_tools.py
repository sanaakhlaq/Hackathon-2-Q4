from sqlmodel import Session, select
from database import engine, get_session # Relative import fix
from models import Todo as Task ,engine

def add_task(title: str, description: str = None):
    with Session(engine) as session:
        new_task = Task(title=title, description=description)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return f"Task '{title}' added successfully!"

def get_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks if tasks else "No tasks found."

def mark_task_complete(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return "Task not found."
        task.is_completed = True
        session.add(task)
        session.commit()
        return f"Task {task_id} marked as completed."

def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return "Task not found."
        session.delete(task)
        session.commit()
        return f"Task {task_id} deleted."