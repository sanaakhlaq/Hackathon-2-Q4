# Internal API Contracts: Phase I – In-Memory Console Todo App

## Overview
This document defines the internal function interfaces for the console todo application. Since this is a single-process console application with no external APIs, these contracts define the internal function signatures and behaviors.

## Core Operations Contracts

### Todo Creation
```python
def add_todo(title: str) -> int:
    """
    Add a new todo to the in-memory store.

    Args:
        title (str): The title/description of the todo item

    Returns:
        int: The unique ID of the newly created todo

    Raises:
        ValueError: If title is empty or contains only whitespace

    Side Effects:
        - Increments the global ID counter
        - Adds a new Todo object to the in-memory store
        - Sets completed=False and created_at to current time automatically
    """
```

### Todo Retrieval
```python
def get_todos() -> List[Todo]:
    """
    Retrieve all todos from the in-memory store.

    Returns:
        List[Todo]: A list of all Todo objects in the store
        Returns empty list if no todos exist

    Raises:
        None

    Side Effects:
        None
    """
```

```python
def get_todo(todo_id: int) -> Optional[Todo]:
    """
    Retrieve a specific todo by its ID.

    Args:
        todo_id (int): The unique ID of the todo to retrieve

    Returns:
        Optional[Todo]: The Todo object if found, None if not found

    Raises:
        None (returns None for invalid IDs)

    Side Effects:
        None
    """
```

### Todo Update
```python
def update_todo(todo_id: int, title: str = None, completed: bool = None) -> bool:
    """
    Update an existing todo's properties.

    Args:
        todo_id (int): The unique ID of the todo to update
        title (str, optional): New title for the todo (if provided)
        completed (bool, optional): New completion status (if provided)

    Returns:
        bool: True if update was successful, False if todo not found

    Raises:
        ValueError: If new title is empty or contains only whitespace

    Side Effects:
        - Modifies the existing Todo object in the in-memory store
        - Only updates provided fields (other fields remain unchanged)
    """
```

### Todo Deletion
```python
def delete_todo(todo_id: int) -> bool:
    """
    Delete a todo by its ID.

    Args:
        todo_id (int): The unique ID of the todo to delete

    Returns:
        bool: True if deletion was successful, False if todo not found

    Raises:
        None (returns False for invalid IDs)

    Side Effects:
        - Removes the Todo object from the in-memory store
        - Updates internal ID mappings
    """
```

### Todo Completion Toggle
```python
def mark_todo_completed(todo_id: int, completed: bool = True) -> bool:
    """
    Mark a todo as completed or incomplete.

    Args:
        todo_id (int): The unique ID of the todo to update
        completed (bool): The new completion status (default True)

    Returns:
        bool: True if update was successful, False if todo not found

    Raises:
        None (returns False for invalid IDs)

    Side Effects:
        - Updates the completed field of the Todo object
    """
```

## Console Interface Contracts

### Menu Display
```python
def display_menu() -> None:
    """
    Display the main menu options to the console.

    Args:
        None

    Returns:
        None

    Raises:
        None

    Side Effects:
        - Prints menu options to stdout
        - Does not read user input
    """
```

### User Input Processing
```python
def handle_user_input() -> None:
    """
    Process user commands from the console interface.

    Args:
        None

    Returns:
        None

    Raises:
        None (errors are handled internally and reported to user)

    Side Effects:
        - Reads input from stdin
        - Calls appropriate operation functions
        - Displays results or error messages to stdout
        - May exit the application based on user choice
    """
```

### Application Entry Point
```python
def main() -> None:
    """
    Main application entry point.

    Args:
        None

    Returns:
        None

    Raises:
        SystemExit: When the application is terminated

    Side Effects:
        - Initializes the application state
        - Starts the main console loop
        - Handles graceful shutdown
    """
```

## Error Handling Contracts

### Validation Errors
- All functions that accept user input validate their parameters
- ValueError is raised for invalid input (e.g., empty titles)
- TypeError is raised for incorrect parameter types
- Error messages are user-friendly and actionable

### Recovery Behavior
- Functions that fail return appropriate falsy values (False, None, empty list)
- The application state remains consistent after errors
- Users are informed of errors and can continue using the application
- No operation should cause the application to crash

## Performance Contracts
- All operations should complete in less than 100ms for reasonable data sizes
- Memory usage should remain proportional to the number of todos
- The application should handle up to 1000 todos efficiently