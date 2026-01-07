"""
Todo data model using dataclasses
"""
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