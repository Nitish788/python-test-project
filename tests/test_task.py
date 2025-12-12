"""Tests for Task model and service."""

import unittest
from datetime import datetime, timedelta
from app.models.task import Task, TaskStatus, TaskPriority
from app.services.task_service import TaskRepository
from app.common.exceptions import ValidationError, NotFoundError


class TestTaskModel(unittest.TestCase):
    """Test cases for Task model."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.task = Task(
            task_id=1,
            title="Test Task",
            description="Test description",
            status=TaskStatus.TODO,
        )

    def test_task_creation(self) -> None:
        """Test task creation."""
        self.assertEqual(self.task.id, 1)
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, TaskStatus.TODO)

    def test_task_validation(self) -> None:
        """Test task validation."""
        is_valid, error = self.task.validate()
        self.assertTrue(is_valid)

    def test_task_validation_empty_title(self) -> None:
        """Test validation with empty title."""
        task = Task(2, "", "description")
        is_valid, error = task.validate()
        self.assertFalse(is_valid)

    def test_mark_as_done(self) -> None:
        """Test marking task as done."""
        self.task.mark_as_done()
        self.assertEqual(self.task.status, TaskStatus.DONE)
        self.assertIsNotNone(self.task.completed_at)

    def test_is_overdue(self) -> None:
        """Test overdue check."""
        past_date = datetime.now() - timedelta(days=1)
        task = Task(3, "Overdue", due_date=past_date)
        self.assertTrue(task.is_overdue())

    def test_add_tag(self) -> None:
        """Test adding tags."""
        self.task.add_tag("important")
        self.assertIn("important", self.task.tags)

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["status"], "todo")


class TestTaskService(unittest.TestCase):
    """Test cases for TaskRepository."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.repo = TaskRepository()

    def test_create_task(self) -> None:
        """Test creating a task."""
        task = self.repo.create("New Task", "Description")
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "New Task")

    def test_create_invalid_task(self) -> None:
        """Test creating invalid task."""
        with self.assertRaises(ValidationError):
            self.repo.create("", "description")

    def test_get_task(self) -> None:
        """Test getting a task."""
        task = self.repo.create("Test", "Desc")
        retrieved = self.repo.get(task.id)
        self.assertEqual(retrieved.title, "Test")

    def test_find_by_status(self) -> None:
        """Test finding tasks by status."""
        self.repo.create("Task 1", status=TaskStatus.TODO)
        self.repo.create("Task 2", status=TaskStatus.IN_PROGRESS)

        todos = self.repo.find_by_status(TaskStatus.TODO)
        self.assertEqual(len(todos), 1)

    def test_count(self) -> None:
        """Test counting tasks."""
        self.repo.create("Task 1")
        self.repo.create("Task 2")
        self.assertEqual(self.repo.count(), 2)


if __name__ == "__main__":
    unittest.main()
