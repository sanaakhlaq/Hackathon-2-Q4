# Data Model: Phase I – In-Memory Console Todo App

## Entities

### Todo Entity

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Required, Unique, Auto-incremented | Unique identifier for the todo |
| title | str | Required, Non-empty | Description/title of the todo item |
| completed | bool | Required, Default: False | Completion status of the todo |
| created_at | datetime | Required, Auto-generated | Timestamp when the todo was created |

#### Relationships
- No relationships needed for this simple model

#### Validation Rules
1. **Title Validation**:
   - Cannot be empty or contain only whitespace
   - Must be a string with length > 0 after stripping whitespace

2. **ID Validation**:
   - Must be a positive integer
   - Must be unique within the application's in-memory store

3. **Completed Validation**:
   - Must be a boolean value (True/False)
   - Defaults to False when creating a new todo

4. **Created_at Validation**:
   - Must be a valid datetime object
   - Automatically set to current time when creating a new todo

#### State Transitions
- **Creation**: When a new todo is added, `completed` is set to False, `created_at` is set to current time
- **Update**: The `title` can be modified, `completed` can be toggled
- **Deletion**: The todo is removed from the in-memory store

## In-Memory Storage Model

### Storage Structure
- **Primary Storage**: Python list of Todo objects
- **ID Management**: Auto-incremented integer counter for unique IDs
- **Indexing**: Dictionary mapping ID to list index for O(1) lookup

### Storage Operations
1. **Create**: Add new Todo object to the list, assign next available ID
2. **Read**: Retrieve Todo by ID using index mapping
3. **Update**: Modify existing Todo object in place
4. **Delete**: Remove Todo from list and update ID mapping

### Data Integrity
- No duplicate IDs allowed
- Consistent state maintained during all operations
- Error handling prevents data corruption

## Implementation Details

### Todo Class Definition
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

        # Validation
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        if not isinstance(self.completed, bool):
            raise TypeError("Completed must be a boolean value")
```

### Storage Class Definition
```python
from typing import List, Dict, Optional
from todo_app.models import Todo

class InMemoryStorage:
    def __init__(self):
        self._todos: List[Todo] = []
        self._id_counter: int = 1
        self._id_to_index: Dict[int, int] = {}

    def add_todo(self, title: str) -> Todo:
        # Creates and adds a new Todo with auto-incremented ID
        pass

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        # Retrieves a Todo by ID
        pass

    def get_all_todos(self) -> List[Todo]:
        # Returns all todos
        pass

    def update_todo(self, todo_id: int, title: str = None, completed: bool = None) -> bool:
        # Updates an existing Todo
        pass

    def delete_todo(self, todo_id: int) -> bool:
        # Deletes a Todo by ID
        pass
```