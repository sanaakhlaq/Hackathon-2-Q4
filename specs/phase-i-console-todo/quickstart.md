# Quickstart Guide: Phase I – In-Memory Console Todo App

## Prerequisites
- Python 3.13 or higher
- UV package manager (optional, for dependency management)

## Setup Instructions

### 1. Clone or Create Project Directory
```bash
# If cloning from repository
git clone <repository-url>
cd <project-directory>

# Or create a new directory for the project
mkdir todo-app
cd todo-app
```

### 2. Verify Python Version
```bash
python --version
# Should show Python 3.13.x
```

### 3. (Optional) Setup UV Package Manager
```bash
# Install UV if not already installed
pip install uv

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Project Structure
After setup, your project should have the following structure:
```
todo-app/
├── todo_app/
│   ├── __init__.py
│   ├── models.py          # Todo data model
│   ├── storage.py         # In-memory storage
│   ├── operations.py      # CRUD operations
│   ├── interface.py       # Console interface
│   └── main.py           # Application entry point
├── specs/                # Specification files
│   └── phase-i-console-todo/
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       └── contracts/
│           └── internal-api-contracts.md
└── README.md
```

## Running the Application

### 1. Navigate to Project Directory
```bash
cd todo-app
```

### 2. Run the Application
```bash
python -m todo_app.main
```

## Using the Console Application

Once the application starts, you'll see a menu with the following options:

1. **Add Todo**: Create a new todo item
2. **View Todos**: List all todos with their status
3. **Update Todo**: Modify an existing todo's title
4. **Delete Todo**: Remove a todo from the list
5. **Mark Todo as Complete/Incomplete**: Toggle completion status
6. **Exit**: Quit the application

### Example Usage Flow:
1. Select "Add Todo" and enter a title for your new todo
2. Select "View Todos" to see your list
3. Select "Mark Todo as Complete/Incomplete" to update status
4. Continue managing your todos
5. Select "Exit" when finished

## Development

### Adding New Features
- Add new functionality to the appropriate module based on the layered architecture
- Maintain separation of concerns (Domain, Logic, Interface)
- Follow the same patterns used in existing code

### Testing
- Manually test all user flows through the console interface
- Verify all CRUD operations work correctly
- Test error handling by providing invalid inputs

## Troubleshooting

### Common Issues:
- **Python Version**: Ensure you're using Python 3.13+
- **Module Not Found**: Run with `-m` flag: `python -m todo_app.main`
- **Permission Errors**: Check that you have read/write access to the project directory

### Error Messages:
- "Title cannot be empty": Provide a non-empty title when adding/updating todos
- "Todo not found": Ensure the ID exists when updating/deleting specific todos