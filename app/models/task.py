"""Task model - demonstrates BaseModel usage."""

from typing import Optional, Dict, Any, Tuple
from enum import Enum
from datetime import datetime
from app.common.base import BaseModel


class TaskStatus(Enum):
    """Task status enumeration."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    """
    Task model.

    Demonstrates BaseModel implementation with validation,
    serialization, and common attributes.
    """

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        project_id: int = 0,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: Optional[datetime] = None,
        assignee_id: Optional[int] = None,
        tags: Optional[list] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialize Task."""
        super().__init__(task_id, created_at)
        self.title = title
        self.description = description
        self.project_id = project_id
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.assignee_id = assignee_id
        self.tags = tags or []
        self.completed_at: Optional[datetime] = None

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate task."""
        if not self.title or len(self.title.strip()) == 0:
            return False, "Title is required"

        if len(self.title) > 255:
            return False, "Title cannot exceed 255 characters"

        if len(self.description) > 2000:
            return False, "Description cannot exceed 2000 characters"

        return True, None

    def mark_as_done(self) -> None:
        """Mark task as done."""
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def mark_as_in_progress(self) -> None:
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and self.status != TaskStatus.DONE:
            return datetime.now() > self.due_date
        return False

    def add_tag(self, tag: str) -> None:
        """Add tag to task."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "project_id": self.project_id,
            "status": self.status.value,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "assignee_id": self.assignee_id,
            "tags": self.tags,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_overdue": self.is_overdue(),
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"Task(id={self.id}, title='{self.title}', status={self.status.value})"
