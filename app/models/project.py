"""Project model - demonstrates BaseModel usage."""

from typing import Optional, Dict, Any, Tuple, List
from enum import Enum
from datetime import datetime
from app.common.base import BaseModel


class ProjectStatus(Enum):
    """Project status enumeration."""

    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(BaseModel):
    """
    Project model.

    Demonstrates BaseModel implementation with its own
    specific validations and methods.
    """

    def __init__(
        self,
        project_id: int,
        name: str,
        description: str = "",
        owner_id: int = 0,
        status: ProjectStatus = ProjectStatus.PLANNING,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialize Project."""
        super().__init__(project_id, created_at)
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.status = status
        self.members: List[int] = [owner_id] if owner_id else []
        self.task_count = 0
        self.completed_task_count = 0

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate project."""
        if not self.name or len(self.name.strip()) == 0:
            return False, "Project name is required"

        if len(self.name) > 100:
            return False, "Project name cannot exceed 100 characters"

        if len(self.description) > 1000:
            return False, "Description cannot exceed 1000 characters"

        return True, None

    def add_member(self, user_id: int) -> bool:
        """Add member to project."""
        if user_id not in self.members:
            self.members.append(user_id)
            self.updated_at = datetime.now()
            return True
        return False

    def remove_member(self, user_id: int) -> bool:
        """Remove member from project."""
        if user_id != self.owner_id and user_id in self.members:
            self.members.remove(user_id)
            self.updated_at = datetime.now()
            return True
        return False

    def activate(self) -> None:
        """Activate project."""
        self.status = ProjectStatus.ACTIVE
        self.updated_at = datetime.now()

    def archive(self) -> None:
        """Archive project."""
        self.status = ProjectStatus.ARCHIVED
        self.updated_at = datetime.now()

    def get_progress(self) -> float:
        """Get project progress as percentage."""
        if self.task_count == 0:
            return 0.0
        return (self.completed_task_count / self.task_count) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "status": self.status.value,
            "members": self.members,
            "task_count": self.task_count,
            "completed_task_count": self.completed_task_count,
            "progress": self.get_progress(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"Project(id={self.id}, name='{self.name}', status={self.status.value})"
