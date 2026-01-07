"""
Main application entry point for the Todo Console App
"""
from .storage import InMemoryStorage
from .operations import TodoOperations
from .interface import TodoInterface


def main():
    """
    Main application entry point.
    Initializes the application state and starts the main console loop.
    """
    # Initialize storage, operations, and interface layers
    storage = InMemoryStorage()
    operations = TodoOperations(storage)
    interface = TodoInterface(operations)

    print("Welcome to the Todo Console Application!")
    print("This is a Phase I in-memory console todo app.")

    # Main application loop
    running = True
    while running:
        try:
            interface.display_menu()
            running = interface.handle_user_input()
        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("The application will continue running.")

    print("Application terminated.")


if __name__ == "__main__":
    main()