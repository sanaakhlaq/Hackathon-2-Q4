"""
Console interface for todo application
"""
from typing import Optional
from .operations import TodoOperations


class TodoInterface:
    def __init__(self, operations: TodoOperations):
        self.operations = operations

    def display_menu(self) -> None:
        """
        Display the main menu options to the console.
        """
        print("\n" + "="*40)
        print("TODO APPLICATION")
        print("="*40)
        print("1. Add Todo")
        print("2. View All Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Todo as Complete/Incomplete")
        print("6. Exit")
        print("="*40)

    def get_user_input(self, prompt: str) -> str:
        """
        Get input from user with a prompt.

        Args:
            prompt (str): The prompt to display

        Returns:
            str: User input
        """
        return input(prompt).strip()

    def handle_add_todo(self) -> None:
        """
        Handle adding a new todo.
        """
        try:
            title = self.get_user_input("Enter todo title: ")
            if not title:
                print("Error: Title cannot be empty!")
                return

            todo_id = self.operations.add_todo(title)
            print(f"Successfully added todo with ID: {todo_id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error adding todo: {e}")

    def handle_view_todos(self) -> None:
        """
        Handle viewing all todos.
        """
        try:
            todos = self.operations.get_todos()
            if not todos:
                print("No todos found.")
                return

            print("\nYour Todos:")
            print("-" * 50)
            for todo in todos:
                status = "✓" if todo.completed else "○"
                print(f"[{status}] ID: {todo.id} | Title: {todo.title} | Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 50)
        except Exception as e:
            print(f"Error viewing todos: {e}")

    def handle_update_todo(self) -> None:
        """
        Handle updating a todo.
        """
        try:
            todo_id_str = self.get_user_input("Enter todo ID to update: ")
            try:
                todo_id = int(todo_id_str)
            except ValueError:
                print("Error: Please enter a valid number for todo ID!")
                return

            # Check if todo exists
            existing_todo = self.operations.get_todo(todo_id)
            if not existing_todo:
                print(f"Error: Todo with ID {todo_id} not found!")
                return

            print(f"Current title: {existing_todo.title}")
            new_title = self.get_user_input("Enter new title (or press Enter to keep current): ")

            # If user pressed Enter without typing anything, keep the current title
            if new_title == "":
                new_title = existing_todo.title

            if not new_title.strip():
                print("Error: Title cannot be empty!")
                return

            success = self.operations.update_todo(todo_id, title=new_title)
            if success:
                print(f"Successfully updated todo with ID: {todo_id}")
            else:
                print(f"Failed to update todo with ID: {todo_id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error updating todo: {e}")

    def handle_delete_todo(self) -> None:
        """
        Handle deleting a todo.
        """
        try:
            todo_id_str = self.get_user_input("Enter todo ID to delete: ")
            try:
                todo_id = int(todo_id_str)
            except ValueError:
                print("Error: Please enter a valid number for todo ID!")
                return

            success = self.operations.delete_todo(todo_id)
            if success:
                print(f"Successfully deleted todo with ID: {todo_id}")
            else:
                print(f"Error: Todo with ID {todo_id} not found!")
        except Exception as e:
            print(f"Unexpected error deleting todo: {e}")

    def handle_toggle_completion(self) -> None:
        """
        Handle marking a todo as complete/incomplete.
        """
        try:
            todo_id_str = self.get_user_input("Enter todo ID to mark: ")
            try:
                todo_id = int(todo_id_str)
            except ValueError:
                print("Error: Please enter a valid number for todo ID!")
                return

            # Check if todo exists
            existing_todo = self.operations.get_todo(todo_id)
            if not existing_todo:
                print(f"Error: Todo with ID {todo_id} not found!")
                return

            current_status = "complete" if existing_todo.completed else "incomplete"
            new_status = "incomplete" if existing_todo.completed else "complete"

            success = self.operations.mark_todo_completed(todo_id, completed=not existing_todo.completed)
            if success:
                print(f"Successfully marked todo with ID {todo_id} as {new_status}")
            else:
                print(f"Failed to update todo with ID: {todo_id}")
        except Exception as e:
            print(f"Unexpected error marking todo: {e}")

    def handle_user_input(self) -> bool:
        """
        Process user commands from the console interface.
        Returns True to continue, False to exit.
        """
        try:
            choice = self.get_user_input("Enter your choice (1-6): ")
            if choice == "1":
                self.handle_add_todo()
            elif choice == "2":
                self.handle_view_todos()
            elif choice == "3":
                self.handle_update_todo()
            elif choice == "4":
                self.handle_delete_todo()
            elif choice == "5":
                self.handle_toggle_completion()
            elif choice == "6":
                print("Thank you for using the Todo App!")
                return False  # Exit the application
            else:
                print("Invalid choice! Please enter a number between 1-6.")
        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return True  # Continue the application