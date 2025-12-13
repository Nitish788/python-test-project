"""Notification service - demonstrates BaseRepository pattern reuse."""

from typing import List, Optional
from app.common.base import BaseRepository
from app.common.exceptions import ValidationError, NotFoundError
from app.models.notification import Notification, NotificationStatus, NotificationType
from app.services.task_service import TaskRepository
import logging

logger = logging.getLogger(__name__)


class NotificationRepository(BaseRepository[Notification]):
    """
    Notification repository.

    Demonstrates reusing BaseRepository pattern established by TaskRepository,
    ProjectRepository, CategoryRepository, TagRepository.
    All repositories follow the same CRUD and validation approach.
    """

    def create(
        self,
        user_id: int,
        message: str,
        notification_type: NotificationType,
        related_entity_id: Optional[int] = None,
        related_entity_type: Optional[str] = None,
    ) -> Notification:
        """
        Create a new notification.

        Args:
            user_id: User who receives notification
            message: Notification message
            notification_type: Type of notification
            related_entity_id: Related entity ID (optional)
            related_entity_type: Related entity type (optional)

        Returns:
            Created notification

        Raises:
            ValidationError: If notification data is invalid
        """
        notification = Notification(
            notification_id=self.get_next_id(),
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            related_entity_id=related_entity_id,
            related_entity_type=related_entity_type,
        )

        # Validate before storing (same pattern as TaskRepository, ProjectRepository)
        is_valid, error = notification.validate()
        if not is_valid:
            raise ValidationError(error)

        self._items[notification.id] = notification
        logger.info(f"Notification created: {notification}")
        return notification

    def find_by_user(self, user_id: int) -> List[Notification]:
        """
        Find all notifications for a user.

        Args:
            user_id: User ID

        Returns:
            List of notifications for user
        """
        return [n for n in self._items.values() if n.user_id == user_id]

    def find_unread(self, user_id: int) -> List[Notification]:
        """
        Find unread notifications for a user.

        Args:
            user_id: User ID

        Returns:
            List of unread notifications
        """
        return [
            n
            for n in self._items.values()
            if n.user_id == user_id and n.status == NotificationStatus.UNREAD
        ]

    def find_by_type(self, notification_type: NotificationType) -> List[Notification]:
        """
        Find notifications by type.

        Args:
            notification_type: Type to filter by

        Returns:
            List of notifications of given type
        """
        return [
            n for n in self._items.values() if n.notification_type == notification_type
        ]

    def mark_as_read(self, notification_id: int) -> Notification:
        """
        Mark notification as read.

        Args:
            notification_id: Notification ID

        Returns:
            Updated notification

        Raises:
            NotFoundError: If notification not found
        """
        notification = self.get(notification_id)
        if not notification:
            raise NotFoundError(f"Notification {notification_id} not found", "Notification")

        notification.mark_as_read()
        logger.info(f"Notification {notification_id} marked as read")
        return notification

    def archive(self, notification_id: int) -> Notification:
        """
        Archive notification.

        Args:
            notification_id: Notification ID

        Returns:
            Archived notification

        Raises:
            NotFoundError: If notification not found
        """
        notification = self.get(notification_id)
        if not notification:
            raise NotFoundError(f"Notification {notification_id} not found", "Notification")

        notification.archive()
        logger.info(f"Notification {notification_id} archived")
        return notification

    def get_unread_count(self, user_id: int) -> int:
        """
        Get count of unread notifications for user.

        Args:
            user_id: User ID

        Returns:
            Number of unread notifications
        """
        return len(self.find_unread(user_id))

    def get_by_type_for_user(
        self, user_id: int, notification_type: NotificationType
    ) -> List[Notification]:
        """
        Find notifications for user of specific type.

        Args:
            user_id: User ID
            notification_type: Notification type

        Returns:
            Filtered notifications
        """
        return [
            n
            for n in self._items.values()
            if n.user_id == user_id and n.notification_type == notification_type
        ]
    
    def get_notification_stats(self):
        """Get notification statistics."""
        notifications = self._items.values()
        total = len(notifications)
        unread = len([n for n in notifications if n.status == NotificationStatus.UNREAD])
        return {"total": total, "unread": unread}
