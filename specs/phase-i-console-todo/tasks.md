# Tasks: Phase I – In-Memory Console Todo App

## Feature Overview
A single-process Python console application with layered structure (Domain: Todo model, Logic: In-memory CRUD operations, Interface: Console I/O loop)

## User Stories
- **US1** (P1): As a user, I want to create todo items so that I can track my tasks
- **US2** (P2): As a user, I want to view my todo items so that I can see what tasks I have
- **US3** (P3): As a user, I want to update my todo items so that I can modify task details
- **US4** (P4): As a user, I want to delete my todo items so that I can remove completed tasks
- **US5** (P5): As a user, I want to mark my todo items as complete/incomplete so that I can track progress

## Phase 1: Setup
**Goal**: Initialize project structure and dependencies

- [x] T001 Create project directory structure with todo_app package
- [x] T002 Create pyproject.toml with Python 3.13+ requirement and UV configuration
- [x] T003 Set up basic file structure: models.py, storage.py, operations.py, interface.py, main.py
- [x] T004 Create .gitignore file for Python project
- [x] T005 [P] Create README.md with project description

## Phase 2: Foundational
**Goal**: Implement core data model and storage infrastructure that all user stories depend on

- [x] T006 Implement Todo dataclass in todo_app/models.py with id, title, completed, created_at fields
- [x] T007 Implement validation in Todo dataclass for title and field types
- [x] T008 Create InMemoryStorage class in todo_app/storage.py with basic structure
- [x] T009 Implement in-memory storage using Python list and ID mapping in storage.py
- [x] T010 Implement auto-incrementing ID counter in storage.py
- [x] T011 Create operations module with function signatures matching contracts

## Phase 3: [US1] Create Todo Items
**Goal**: Implement functionality to create new todo items
**Independent Test Criteria**: User can add a new todo with a title and see it assigned a unique ID

- [x] T012 [P] [US1] Implement add_todo function in operations.py that creates new Todo
- [x] T013 [P] [US1] Implement storage add method to insert Todo in the store
- [x] T014 [US1] Implement console interface for adding new todos in interface.py
- [x] T015 [US1] Add input validation for new todo titles (non-empty check)
- [x] T016 [US1] Implement error handling for invalid todo creation

## Phase 4: [US2] View Todo Items
**Goal**: Implement functionality to view all todo items
**Independent Test Criteria**: User can view a list of all todos with their status

- [x] T017 [P] [US2] Implement get_todos function in operations.py to retrieve all todos
- [x] T018 [P] [US2] Implement get_todo function in operations.py to retrieve single todo
- [x] T019 [US2] Implement storage methods to retrieve todos
- [x] T020 [US2] Implement console interface for displaying todos in interface.py
- [x] T021 [US2] Format display to show todo ID, title, and completion status

## Phase 5: [US3] Update Todo Items
**Goal**: Implement functionality to update existing todo items
**Independent Test Criteria**: User can update the title of an existing todo

- [x] T022 [P] [US3] Implement update_todo function in operations.py
- [x] T023 [US3] Implement storage update method to modify existing todo
- [x] T024 [US3] Implement console interface for updating todos in interface.py
- [x] T025 [US3] Add validation for updated todo titles (non-empty check)
- [x] T026 [US3] Handle case where todo to update doesn't exist

## Phase 6: [US4] Delete Todo Items
**Goal**: Implement functionality to delete todo items
**Independent Test Criteria**: User can delete a todo by its ID

- [x] T027 [P] [US4] Implement delete_todo function in operations.py
- [x] T028 [US4] Implement storage delete method to remove todo from store
- [x] T029 [US4] Update ID mappings when a todo is deleted
- [x] T030 [US4] Implement console interface for deleting todos in interface.py
- [x] T031 [US4] Handle case where todo to delete doesn't exist

## Phase 7: [US5] Mark Todo Complete/Incomplete
**Goal**: Implement functionality to toggle completion status of todo items
**Independent Test Criteria**: User can mark a todo as complete or incomplete

- [x] T032 [P] [US5] Implement mark_todo_completed function in operations.py
- [x] T033 [US5] Update storage to support completion status modification
- [x] T034 [US5] Implement console interface for toggling completion status
- [x] T035 [US5] Handle case where todo to update doesn't exist

## Phase 8: Console Interface & Menu System
**Goal**: Implement the main console interface with menu system

- [x] T036 Implement display_menu function in interface.py with all options
- [x] T037 Implement handle_user_input function to process menu selections
- [x] T038 Create main application loop in main.py
- [x] T039 Implement graceful exit functionality
- [x] T040 Add error handling for user input validation
- [x] T041 [P] Implement clear user prompts and instructions

## Phase 9: Polish & Cross-Cutting Concerns
**Goal**: Complete the application with error handling, documentation, and testing

- [x] T042 Add comprehensive error handling throughout the application
- [x] T043 Implement consistent error messages for all operations
- [x] T044 Add type hints to all functions and classes
- [x] T045 Write docstrings for all functions and classes
- [x] T046 Implement input validation for all user inputs
- [x] T047 [P] Create requirements.txt or uv.lock file
- [x] T048 Manual testing of all user flows
- [x] T049 Code cleanup and formatting with consistent style
- [x] T050 Final integration testing of all features

## Dependencies
- User Story 1 (Create) must be completed before User Stories 3, 4, 5 (Update, Delete, Mark Complete) can be fully tested
- Foundational phase must be completed before any user story phases

## Parallel Execution Examples
- T012, T017 can run in parallel (different functions in operations.py)
- T014, T020, T024, T030 can run in parallel (different console interfaces)
- T001, T002, T005 can run in parallel (different setup tasks)

## Implementation Strategy
- MVP approach: Complete US1 (Create) first to establish core functionality
- Incrementally add features following user story order
- Each user story should be independently testable before moving to the next