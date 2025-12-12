"""Project service - demonstrates BaseRepository usage."""

from typing import List
from app.common.base import BaseRepository
from app.common.exceptions import ValidationError
from app.models.project import Project, ProjectStatus
import logging

logger = logging.getLogger(__name__)


class ProjectRepository(BaseRepository[Project]):
    """Repository for managing projects."""

    def create(
        self,
        name: str,
        description: str = "",
        owner_id: int = 0,
        status: ProjectStatus = ProjectStatus.PLANNING,
    ) -> Project:
        """
        Create a new project.

        Args:
            name: Project name
            description: Project description
            owner_id: Project owner ID
            status: Project status

        Returns:
            Created project

        Raises:
            ValidationError: If project data is invalid
        """
        project = Project(
            project_id=self.get_next_id(),
            name=name,
            description=description,
            owner_id=owner_id,
            status=status,
        )

        # Validate before storing
        is_valid, error = project.validate()
        if not is_valid:
            raise ValidationError(error)

        self._items[project.id] = project
        logger.info(f"Project created: {project}")
        return project

    def find_by_owner(self, owner_id: int) -> List[Project]:
        """Find projects by owner ID."""
        return [p for p in self._items.values() if p.owner_id == owner_id]

    def find_by_status(self, status: ProjectStatus) -> List[Project]:
        """Find projects by status."""
        return [p for p in self._items.values() if p.status == status]

    def find_active(self) -> List[Project]:
        """Find all active projects."""
        return self.find_by_status(ProjectStatus.ACTIVE)

    def get_user_projects(self, user_id: int) -> List[Project]:
        """Get all projects where user is a member."""
        return [p for p in self._items.values() if user_id in p.members]
