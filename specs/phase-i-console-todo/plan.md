# Implementation Plan: Phase I – In-Memory Console Todo App

## Feature Specification Reference
- **Feature**: Phase I – In-Memory Console Todo App
- **Description**: Single-process Python console application with layered structure (Domain: Todo model, Logic: In-memory CRUD operations, Interface: Console I/O loop)

## Technical Context
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Architecture**: Single-process console application with layered structure
- **Data Storage**: In-memory only (no files, no database)
- **Dependencies**: Standard library only (no external dependencies)
- **User Interface**: Console-based with menu and command loop
- **Scope**: Single-user, deterministic flow

## Constitution Check
Based on `.specify/memory/constitution.md`:

### Phase Standards Compliance
- ✅ **Phase I – In-Memory Console Application**:
  - Language: Python (✓ Python 3.13+)
  - Interface: Console-based (✓ Console menu and command loop)
  - Data storage: In-memory only (✓ No files, no database)
  - Features: Create, read, update, delete todos (✓ Planned in implementation)
  - Code must be: Simple, Modular, Beginner-readable (✓ Following YAGNI principles)
  - No external dependencies beyond standard library (✓ Planned)

### Core Principles Alignment
- ✅ **Correctness First**: Functionality must work as specified in each phase
- ✅ **Incremental Evolution**: Each phase builds cleanly on the previous one
- ✅ **Simplicity Before Abstraction**: Prioritize simple solutions over complex abstractions
- ✅ **Clear Separation of Concerns**: Maintain separation between UI, logic, data
- ✅ **Production-Readiness Mindset**: Not applicable until Phase II+
- ✅ **AI Safety and Determinism**: Not applicable until Phase III+

### Quality Standards Alignment
- ✅ Code clarity over cleverness
- ✅ Reproducibility of setup, execution, and deployment
- ✅ Clear separation of concerns (UI, logic, data)
- ✅ Incremental evolution: each phase builds cleanly on the previous one
- ✅ Correctness first: functionality must work as specified in each phase

## Gates Evaluation
- ✅ **Architecture Compliance**: Matches Phase I standards
- ✅ **Dependency Compliance**: No external dependencies beyond standard library
- ✅ **Scope Compliance**: Within Phase I boundaries
- ✅ **Technology Compliance**: Python 3.13+ with UV package manager

## Phase 0: Outline & Research

### Research Tasks
1. Python 3.13+ best practices for console applications
2. In-memory data structure options for todo storage
3. Console input validation and error handling patterns
4. Clean project structure organization for Python CLI apps

### Research Findings
**Decision**: Use Python's dataclasses for Todo model, built-in list for in-memory storage
**Rationale**: Simple, readable, follows Python conventions, beginner-friendly
**Alternatives considered**: Named tuples, regular classes, dictionaries

**Decision**: Use simple while loop for console menu system
**Rationale**: Straightforward implementation, easy to understand, meets requirements
**Alternatives considered**: argparse for command-line arguments, curses for advanced UI

**Decision**: Use try/except blocks for input validation and error handling
**Rationale**: Python's idiomatic error handling approach, clear and readable
**Alternatives considered**: Manual validation checks, custom validation functions

## Phase 1: Design & Contracts

### Data Model (data-model.md)

#### Todo Entity
- **id**: int (unique identifier, auto-incremented)
- **title**: str (todo description, required)
- **completed**: bool (completion status, default False)
- **created_at**: datetime (timestamp of creation, auto-generated)

#### Relationships
- No relationships needed for this simple model

#### Validation Rules
- title must not be empty or whitespace-only
- id must be unique within the application
- completed must be boolean

### API Contracts

Since this is a console application without external APIs, contracts are internal function interfaces:

#### Core Functions
```python
def add_todo(title: str) -> int:
    """Add a new todo and return its ID"""
    pass

def get_todos() -> List[Todo]:
    """Get all todos"""
    pass

def update_todo(todo_id: int, title: str = None, completed: bool = None) -> bool:
    """Update an existing todo, return success status"""
    pass

def delete_todo(todo_id: int) -> bool:
    """Delete a todo by ID, return success status"""
    pass

def mark_todo_completed(todo_id: int, completed: bool = True) -> bool:
    """Mark a todo as completed/incomplete, return success status"""
    pass
```

#### Console Interface Functions
```python
def display_menu() -> None:
    """Display the main menu options"""
    pass

def handle_user_input() -> None:
    """Process user commands from console"""
    pass
```

### Quickstart Guide

1. Clone the repository
2. Ensure Python 3.13+ is installed
3. Install dependencies: `uv sync` (if any)
4. Run the application: `python -m todo_app.main`
5. Follow the console prompts to manage your todos

### Agent Context Update
- New technology: Python console application patterns
- Architecture: Layered architecture (Domain, Logic, Interface)
- Data structures: In-memory storage using built-in Python types

## Implementation Roadmap

### Stage 1: Core Data Model
- Define Todo dataclass
- Implement basic in-memory storage

### Stage 2: Business Logic
- Implement CRUD operations
- Add input validation

### Stage 3: Console Interface
- Build menu system
- Implement command loop
- Add error handling

### Stage 4: Testing & Polish
- Manual testing of all flows
- Error handling verification
- Code cleanup and documentation

## Risks & Mitigations
- **Risk**: Input validation issues
  - **Mitigation**: Comprehensive validation with clear error messages
- **Risk**: Memory management with large todo lists
  - **Mitigation**: Not applicable - this is a demo application with limited scope
- **Risk**: User confusion with console interface
  - **Mitigation**: Clear prompts and instructions

## Success Criteria
- All CRUD operations work correctly
- Console interface is intuitive and user-friendly
- Error handling prevents crashes
- Application follows Phase I constitution standards
- Code is beginner-readable and well-organized