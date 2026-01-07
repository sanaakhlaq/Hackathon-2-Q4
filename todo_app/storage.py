"""
In-memory storage for todos
"""
from typing import List, Dict, Optional
from .models import Todo


class InMemoryStorage:
    def __init__(self):
        self._todos: List[Todo] = []
        self._id_counter: int = 1
        self._id_to_index: Dict[int, int] = {}

    def add_todo(self, title: str) -> Todo:
        """
        Add a new todo to the in-memory store.

        Args:
            title (str): The title/description of the todo item

        Returns:
            Todo: The newly created Todo object
        """
        # Create new Todo with auto-incremented ID
        new_todo = Todo(
            id=self._id_counter,
            title=title,
            completed=False
        )

        # Add to storage
        self._todos.append(new_todo)
        self._id_to_index[new_todo.id] = len(self._todos) - 1

        # Increment ID counter
        self._id_counter += 1

        return new_todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific todo by its ID.

        Args:
            todo_id (int): The unique ID of the todo to retrieve

        Returns:
            Optional[Todo]: The Todo object if found, None if not found
        """
        if todo_id in self._id_to_index:
            index = self._id_to_index[todo_id]
            if 0 <= index < len(self._todos):
                return self._todos[index]
        return None

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all todos from the in-memory store.

        Returns:
            List[Todo]: A list of all Todo objects in the store
        """
        return self._todos.copy()

    def update_todo(self, todo_id: int, title: str = None, completed: bool = None) -> bool:
        """
        Update an existing todo's properties.

        Args:
            todo_id (int): The unique ID of the todo to update
            title (str, optional): New title for the todo (if provided)
            completed (bool, optional): New completion status (if provided)

        Returns:
            bool: True if update was successful, False if todo not found
        """
        if todo_id not in self._id_to_index:
            return False

        index = self._id_to_index[todo_id]
        if index >= len(self._todos):
            return False

        todo = self._todos[index]

        # Update title if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty or whitespace-only")
            todo.title = title

        # Update completed status if provided
        if completed is not None:
            if not isinstance(completed, bool):
                raise TypeError("Completed must be a boolean value")
            todo.completed = completed

        return True

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            todo_id (int): The unique ID of the todo to delete

        Returns:
            bool: True if deletion was successful, False if todo not found
        """
        if todo_id not in self._id_to_index:
            return False

        index = self._id_to_index[todo_id]
        if index >= len(self._todos):
            return False

        # Remove from todos list
        del self._todos[index]

        # Update indices in the mapping after the deleted index
        # Shift all mappings for indices after the deleted one
        keys_to_update = []
        for key, idx in self._id_to_index.items():
            if idx > index:
                keys_to_update.append(key)

        for key in keys_to_update:
            self._id_to_index[key] -= 1

        # Remove the deleted todo's ID from the mapping
        del self._id_to_index[todo_id]

        return True