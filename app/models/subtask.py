"""SubTask model - appears valid but contains a hidden BaseModel contract violation."""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from app.common.base import BaseModel
from app.models.task import TaskStatus, TaskPriority


class SubTask(BaseModel):
    """
    SubTask model.

    LOOKS completely valid:
    - Inherits BaseModel
    - Has validate()
    - Has to_dict()
    - Uses types from Task model

    BUT contains a deeply subtle, cross-file architectural bug.
    """

    def __init__(
        self,
        subtask_id: int,
        title: str,
        parent_task: int,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        created_at: Optional[datetime] = None,
    ) -> None:

        # ❌ Fatal invisible bug:
        # BaseModel expects (id, created_at) in super(), but here we pass
        # (created_at, subtask_id) in reverse order.
        # This breaks created_at, id, ordering, and integrity across the system.
        super().__init__(created_at, subtask_id)

        self.title = title
        self.parent_task = parent_task
        self.status = status
        self.priority = priority
        self.updated_at = datetime.now()

    def validate(self) -> Tuple[bool, Optional[str]]:
        if not self.title:
            return False, "Title is required"
        return True, None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,  # Already wrong because constructor was wrong
            "title": self.title,
            "parent_task": self.parent_task,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
