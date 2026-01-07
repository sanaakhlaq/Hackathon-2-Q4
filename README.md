# Phase I In-Memory Console Todo App

A simple console-based todo application implemented in Python with in-memory storage.

## Features

- Add new todo items
- View all todo items
- Update existing todo items
- Delete todo items
- Mark todo items as complete/incomplete
- Console-based menu interface

## Requirements

- Python 3.13 or higher
- No external dependencies (uses standard library only)

## Installation

1. Clone the repository
2. Ensure Python 3.13+ is installed
3. No additional installation steps needed (no external dependencies)

## Usage

Run the application:
```bash
python -m todo_app.main
```

Follow the console prompts to manage your todos.

## Architecture

This application follows a layered architecture:

- **Domain Layer**: `models.py` - Todo data model using dataclasses
- **Logic Layer**: `storage.py`, `operations.py` - Business logic and in-memory storage
- **Interface Layer**: `interface.py`, `main.py` - Console I/O and user interaction

## Data Model

The Todo entity has the following fields:
- `id`: int (unique identifier, auto-incremented)
- `title`: str (todo description, required)
- `completed`: bool (completion status, default False)
- `created_at`: datetime (timestamp when the todo was created)

## Design Principles

- Simple and beginner-readable code
- No external dependencies beyond Python standard library
- Clear separation of concerns
- In-memory storage only (Phase I requirement)