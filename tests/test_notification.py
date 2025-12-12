"""Tests for Notification model and service."""

import unittest
from app.models.notification import Notification, NotificationStatus, NotificationType
from app.services.notification_service import NotificationRepository
from app.common.exceptions import ValidationError, NotFoundError


class TestNotificationModel(unittest.TestCase):
    """Test cases for Notification model - demonstrates BaseModel pattern."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.notification = Notification(
            notification_id=1,
            user_id=1,
            message="Task assigned to you",
            notification_type=NotificationType.TASK_ASSIGNED,
        )

    def test_notification_creation(self) -> None:
        """Test notification creation."""
        self.assertEqual(self.notification.id, 1)
        self.assertEqual(self.notification.user_id, 1)
        self.assertEqual(self.notification.status, NotificationStatus.UNREAD)
        self.assertEqual(self.notification.notification_type, NotificationType.TASK_ASSIGNED)

    def test_notification_validation_passes(self) -> None:
        """Test valid notification passes validation."""
        is_valid, error = self.notification.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_notification_validation_short_message(self) -> None:
        """Test validation fails with short message."""
        notification = Notification(
            notification_id=2,
            user_id=1,
            message="AB",
            notification_type=NotificationType.TASK_ASSIGNED,
        )
        is_valid, error = notification.validate()
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_notification_validation_empty_message(self) -> None:
        """Test validation fails with empty message."""
        notification = Notification(
            notification_id=3,
            user_id=1,
            message="",
            notification_type=NotificationType.TASK_ASSIGNED,
        )
        is_valid, error = notification.validate()
        self.assertFalse(is_valid)

    def test_mark_as_read(self) -> None:
        """Test marking notification as read."""
        self.assertEqual(self.notification.status, NotificationStatus.UNREAD)
        self.notification.mark_as_read()
        self.assertEqual(self.notification.status, NotificationStatus.READ)

    def test_archive(self) -> None:
        """Test archiving notification."""
        self.notification.archive()
        self.assertEqual(self.notification.status, NotificationStatus.ARCHIVED)

    def test_notification_to_dict(self) -> None:
        """Test notification serialization - consistent format."""
        result = self.notification.to_dict()
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["user_id"], 1)
        self.assertEqual(result["message"], "Task assigned to you")
        self.assertEqual(result["status"], "unread")
        self.assertEqual(result["notification_type"], "task_assigned")
        self.assertIn("created_at", result)
        self.assertIn("updated_at", result)

    def test_notification_with_related_entity(self) -> None:
        """Test notification with related entity."""
        notification = Notification(
            notification_id=4,
            user_id=2,
            message="Task completed",
            notification_type=NotificationType.TASK_COMPLETED,
            related_entity_id=101,
            related_entity_type="task",
        )
        result = notification.to_dict()
        self.assertEqual(result["related_entity_id"], 101)
        self.assertEqual(result["related_entity_type"], "task")

    def test_notification_repr(self) -> None:
        """Test notification string representation."""
        repr_str = repr(self.notification)
        self.assertIn("Notification", repr_str)
        self.assertIn("user_id=1", repr_str)


class TestNotificationRepository(unittest.TestCase):
    """Test cases for NotificationRepository - demonstrates BaseRepository pattern."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.repo = NotificationRepository()

    def test_create_notification(self) -> None:
        """Test creating a notification with validation."""
        notification = self.repo.create(
            user_id=1,
            message="New task assigned",
            notification_type=NotificationType.TASK_ASSIGNED,
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user_id, 1)
        self.assertEqual(notification.message, "New task assigned")
        self.assertEqual(notification.status, NotificationStatus.UNREAD)

    def test_create_invalid_notification_short_message(self) -> None:
        """Test creating invalid notification raises ValidationError."""
        with self.assertRaises(ValidationError):
            self.repo.create(
                user_id=1,
                message="AB",
                notification_type=NotificationType.TASK_ASSIGNED,
            )

    def test_create_invalid_notification_empty_message(self) -> None:
        """Test creating notification with empty message."""
        with self.assertRaises(ValidationError):
            self.repo.create(
                user_id=1,
                message="",
                notification_type=NotificationType.TASK_ASSIGNED,
            )

    def test_get_notification(self) -> None:
        """Test getting a notification by ID."""
        created = self.repo.create(1, "Message", NotificationType.TASK_ASSIGNED)
        retrieved = self.repo.get(created.id)
        self.assertEqual(retrieved.id, created.id)
        self.assertEqual(retrieved.message, "Message")

    def test_find_by_user(self) -> None:
        """Test finding notifications by user."""
        self.repo.create(1, "Message 1", NotificationType.TASK_ASSIGNED)
        self.repo.create(1, "Message 2", NotificationType.TASK_COMPLETED)
        self.repo.create(2, "Message 3", NotificationType.TASK_DUE_SOON)

        user1_notifications = self.repo.find_by_user(1)
        self.assertEqual(len(user1_notifications), 2)

        user2_notifications = self.repo.find_by_user(2)
        self.assertEqual(len(user2_notifications), 1)

    def test_find_unread(self) -> None:
        """Test finding unread notifications."""
        n1 = self.repo.create(1, "Message 1", NotificationType.TASK_ASSIGNED)
        n2 = self.repo.create(1, "Message 2", NotificationType.TASK_COMPLETED)

        unread = self.repo.find_unread(1)
        self.assertEqual(len(unread), 2)

        self.repo.mark_as_read(n1.id)
        unread = self.repo.find_unread(1)
        self.assertEqual(len(unread), 1)

    def test_find_by_type(self) -> None:
        """Test finding notifications by type."""
        self.repo.create(1, "Assigned", NotificationType.TASK_ASSIGNED)
        self.repo.create(1, "Completed", NotificationType.TASK_COMPLETED)
        self.repo.create(1, "Due soon", NotificationType.TASK_DUE_SOON)

        assigned = self.repo.find_by_type(NotificationType.TASK_ASSIGNED)
        self.assertEqual(len(assigned), 1)
        self.assertEqual(assigned[0].message, "Assigned")

    def test_mark_as_read(self) -> None:
        """Test marking notification as read."""
        notification = self.repo.create(1, "Message", NotificationType.TASK_ASSIGNED)
        self.repo.mark_as_read(notification.id)

        updated = self.repo.get(notification.id)
        self.assertEqual(updated.status, NotificationStatus.READ)

    def test_mark_nonexistent_as_read(self) -> None:
        """Test marking nonexistent notification raises NotFoundError."""
        with self.assertRaises(NotFoundError):
            self.repo.mark_as_read(999)

    def test_archive(self) -> None:
        """Test archiving notification."""
        notification = self.repo.create(1, "Message", NotificationType.TASK_ASSIGNED)
        self.repo.archive(notification.id)

        updated = self.repo.get(notification.id)
        self.assertEqual(updated.status, NotificationStatus.ARCHIVED)

    def test_archive_nonexistent(self) -> None:
        """Test archiving nonexistent notification raises NotFoundError."""
        with self.assertRaises(NotFoundError):
            self.repo.archive(999)

    def test_get_unread_count(self) -> None:
        """Test getting unread count."""
        self.repo.create(1, "Message 1", NotificationType.TASK_ASSIGNED)
        self.repo.create(1, "Message 2", NotificationType.TASK_COMPLETED)

        count = self.repo.get_unread_count(1)
        self.assertEqual(count, 2)

        # Mark one as read
        notifications = self.repo.find_by_user(1)
        self.repo.mark_as_read(notifications[0].id)

        count = self.repo.get_unread_count(1)
        self.assertEqual(count, 1)

    def test_get_by_type_for_user(self) -> None:
        """Test finding notifications by type for specific user."""
        self.repo.create(1, "Assigned", NotificationType.TASK_ASSIGNED)
        self.repo.create(1, "Completed", NotificationType.TASK_COMPLETED)
        self.repo.create(2, "Assigned", NotificationType.TASK_ASSIGNED)

        user1_assigned = self.repo.get_by_type_for_user(1, NotificationType.TASK_ASSIGNED)
        self.assertEqual(len(user1_assigned), 1)

    def test_count(self) -> None:
        """Test counting notifications."""
        self.repo.create(1, "Message 1", NotificationType.TASK_ASSIGNED)
        self.repo.create(2, "Message 2", NotificationType.TASK_COMPLETED)
        self.assertEqual(self.repo.count(), 2)

    def test_delete(self) -> None:
        """Test deleting notification."""
        notification = self.repo.create(1, "Message", NotificationType.TASK_ASSIGNED)
        result = self.repo.delete(notification.id)
        self.assertTrue(result)
        self.assertIsNone(self.repo.get(notification.id))


if __name__ == "__main__":
    unittest.main()
