"""Tests for Project model and service."""

import unittest
from app.models.project import Project, ProjectStatus
from app.services.project_service import ProjectRepository
from app.common.exceptions import ValidationError


class TestProjectModel(unittest.TestCase):
    """Test cases for Project model."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.project = Project(
            project_id=1,
            name="Test Project",
            owner_id=1,
        )

    def test_project_creation(self) -> None:
        """Test project creation."""
        self.assertEqual(self.project.id, 1)
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.owner_id, 1)

    def test_add_member(self) -> None:
        """Test adding members."""
        result = self.project.add_member(2)
        self.assertTrue(result)
        self.assertIn(2, self.project.members)

    def test_remove_member(self) -> None:
        """Test removing members."""
        self.project.add_member(2)
        result = self.project.remove_member(2)
        self.assertTrue(result)

    def test_activate_project(self) -> None:
        """Test activating project."""
        self.project.activate()
        self.assertEqual(self.project.status, ProjectStatus.ACTIVE)

    def test_get_progress(self) -> None:
        """Test progress calculation."""
        self.project.task_count = 10
        self.project.completed_task_count = 5
        self.assertEqual(self.project.get_progress(), 50.0)

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        proj_dict = self.project.to_dict()
        self.assertEqual(proj_dict["name"], "Test Project")
        self.assertEqual(proj_dict["status"], "planning")


class TestProjectService(unittest.TestCase):
    """Test cases for ProjectRepository."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.repo = ProjectRepository()

    def test_create_project(self) -> None:
        """Test creating a project."""
        project = self.repo.create("New Project", owner_id=1)
        self.assertIsNotNone(project)
        self.assertEqual(project.name, "New Project")

    def test_find_by_status(self) -> None:
        """Test finding projects by status."""
        self.repo.create("Active", status=ProjectStatus.ACTIVE)
        self.repo.create("Planning", status=ProjectStatus.PLANNING)

        active = self.repo.find_by_status(ProjectStatus.ACTIVE)
        self.assertEqual(len(active), 1)

    def test_find_by_owner(self) -> None:
        """Test finding projects by owner."""
        self.repo.create("Project 1", owner_id=1)
        self.repo.create("Project 2", owner_id=2)

        owner1_projects = self.repo.find_by_owner(1)
        self.assertEqual(len(owner1_projects), 1)


if __name__ == "__main__":
    unittest.main()
