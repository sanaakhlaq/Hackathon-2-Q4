"""
Business logic operations for todo management
"""
from typing import List, Optional
from .models import Todo
from .storage import InMemoryStorage


class TodoOperations:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def add_todo(self, title: str) -> int:
        """
        Add a new todo and return its ID.

        Args:
            title (str): The title/description of the todo item

        Returns:
            int: The unique ID of the newly created todo
        """
        new_todo = self.storage.add_todo(title)
        return new_todo.id

    def get_todos(self) -> List[Todo]:
        """
        Get all todos.

        Returns:
            List[Todo]: List of all Todo objects
        """
        return self.storage.get_all_todos()

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Get a specific todo by ID.

        Args:
            todo_id (int): The ID of the todo to retrieve

        Returns:
            Optional[Todo]: The Todo object if found, None otherwise
        """
        return self.storage.get_todo(todo_id)

    def update_todo(self, todo_id: int, title: str = None, completed: bool = None) -> bool:
        """
        Update an existing todo, return success status.

        Args:
            todo_id (int): The ID of the todo to update
            title (str, optional): New title for the todo
            completed (bool, optional): New completion status

        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.storage.update_todo(todo_id, title, completed)

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by ID, return success status.

        Args:
            todo_id (int): The ID of the todo to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        return self.storage.delete_todo(todo_id)

    def mark_todo_completed(self, todo_id: int, completed: bool = True) -> bool:
        """
        Mark a todo as completed/incomplete, return success status.

        Args:
            todo_id (int): The ID of the todo to update
            completed (bool): The new completion status

        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.storage.update_todo(todo_id, completed=completed)