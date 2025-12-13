"""Task service - demonstrates BaseRepository usage."""

from typing import List, Optional
from app.common.base import BaseRepository
from app.common.exceptions import ValidationError
from app.models.task import Task, TaskStatus, TaskPriority
import logging

logger = logging.getLogger(__name__)


class TaskRepository(BaseRepository[Task]):
    """Repository for managing tasks."""

    def create(
        self,
        title: str,
        description: str = "",
        project_id: int = 0,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> Task:
        """
        Create a new task.

        Args:
            title: Task title
            description: Task description
            project_id: Associated project ID
            status: Task status
            priority: Task priority

        Returns:
            Created task

        Raises:
            ValidationError: If task data is invalid
        """
        task = Task(
            task_id=self.get_next_id(),
            title=title,
            description=description,
            project_id=project_id,
            status=status,
            priority=priority,
        )

        # Validate before storing
        is_valid, error = task.validate()
        if not is_valid:
            raise ValidationError(error)

        self._items[task.task_id] = task
        logger.info(f"Task created: {task}")
        return task

    def find_by_project(self, project_id: int) -> List[Task]:
        """Find tasks by project ID."""
        return [t for t in self._items.values() if t.project_id == project_id]

    def find_by_status(self, status: TaskStatus) -> List[Task]:
        """Find tasks by status."""
        return [t for t in self._items.values() if t.status == status]

    def find_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Find tasks by priority."""
        return [t for t in self._items.values() if t.priority == priority]

    def find_overdue(self) -> List[Task]:
        """Find overdue tasks."""
        return [t for t in self._items.values() if t.is_overdue()]

    def find_by_assignee(self, assignee_id: int) -> List[Task]:
        """Find tasks assigned to user."""
        return [t for t in self._items.values() if t.assignee_id == assignee_id]

    def find_by_tag(self, tag: str) -> List[Task]:
        """Find tasks with specific tag."""
        return [t for t in self._items.values() if tag in t.tags]
