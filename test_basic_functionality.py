"""
Basic functionality test for the Todo Console App
"""
from todo_app.storage import InMemoryStorage
from todo_app.operations import TodoOperations
from todo_app.models import Todo


def test_basic_functionality():
    """Test all basic functionality of the todo app"""
    print("Testing basic functionality...")

    # Initialize the application components
    storage = InMemoryStorage()
    operations = TodoOperations(storage)

    # Test 1: Add a todo
    print("\n1. Testing add todo...")
    todo_id = operations.add_todo("Test todo item")
    print(f"Added todo with ID: {todo_id}")

    # Test 2: Get all todos
    print("\n2. Testing get all todos...")
    todos = operations.get_todos()
    print(f"Retrieved {len(todos)} todos")
    for todo in todos:
        print(f"  - ID: {todo.id}, Title: {todo.title}, Completed: {todo.completed}")

    # Test 3: Get specific todo
    print("\n3. Testing get specific todo...")
    specific_todo = operations.get_todo(todo_id)
    if specific_todo:
        print(f"Found todo: ID {specific_todo.id}, Title: {specific_todo.title}")
    else:
        print("Todo not found!")

    # Test 4: Update todo
    print("\n4. Testing update todo...")
    update_success = operations.update_todo(todo_id, title="Updated todo item")
    if update_success:
        print("Todo updated successfully")
        updated_todo = operations.get_todo(todo_id)
        print(f"Updated todo: ID {updated_todo.id}, Title: {updated_todo.title}")
    else:
        print("Failed to update todo")

    # Test 5: Mark as complete
    print("\n5. Testing mark as complete...")
    mark_success = operations.mark_todo_completed(todo_id, completed=True)
    if mark_success:
        print("Todo marked as complete successfully")
        marked_todo = operations.get_todo(todo_id)
        print(f"Marked todo: ID {marked_todo.id}, Completed: {marked_todo.completed}")
    else:
        print("Failed to mark todo as complete")

    # Test 6: Mark as incomplete
    print("\n6. Testing mark as incomplete...")
    mark_success = operations.mark_todo_completed(todo_id, completed=False)
    if mark_success:
        print("Todo marked as incomplete successfully")
        marked_todo = operations.get_todo(todo_id)
        print(f"Marked todo: ID {marked_todo.id}, Completed: {marked_todo.completed}")
    else:
        print("Failed to mark todo as incomplete")

    # Test 7: Delete todo
    print("\n7. Testing delete todo...")
    delete_success = operations.delete_todo(todo_id)
    if delete_success:
        print("Todo deleted successfully")
        deleted_todo = operations.get_todo(todo_id)
        if not deleted_todo:
            print("Confirmed: Todo no longer exists")
        else:
            print("Error: Todo still exists after deletion")
    else:
        print("Failed to delete todo")

    # Test 8: Verify deletion
    print("\n8. Testing verification after deletion...")
    todos_after = operations.get_todos()
    print(f"Remaining todos: {len(todos_after)}")

    print("\nAll basic functionality tests completed!")


if __name__ == "__main__":
    test_basic_functionality()