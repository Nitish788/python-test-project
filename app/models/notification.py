"""Notification model - demonstrates BaseModel pattern reuse."""

from typing import Optional, Dict, Any, Tuple
from enum import Enum
from datetime import datetime
from app.common.base import BaseModel


class NotificationStatus(Enum):
    """Notification status enumeration."""

    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


class NotificationType(Enum):
    """Notification type enumeration."""

    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    TASK_DUE_SOON = "task_due_soon"
    PROJECT_UPDATED = "project_updated"
    COMMENT_ADDED = "comment_added"


class Notification(BaseModel):
    """
    Notification model.

    Demonstrates reusing BaseModel pattern established by Task, Project, Category, Tag.
    All models follow the same structure and validation approach.
    """

    def __init__(
        self,
        notification_id: int,
        user_id: int,
        message: str,
        notification_type: NotificationType,
        status: NotificationStatus = NotificationStatus.UNREAD,
        related_entity_id: Optional[int] = None,
        related_entity_type: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """
        Initialize Notification.

        Args:
            notification_id: Unique notification ID
            user_id: User who should receive notification
            message: Notification message
            notification_type: Type of notification
            status: Current status (default UNREAD)
            related_entity_id: ID of related entity (task, project, etc.)
            related_entity_type: Type of related entity
            created_at: Creation timestamp
        """
        super().__init__(notification_id, created_at)
        self.user_id = user_id
        self.message = message
        self.notification_type = notification_type
        self.status = status
        self.related_entity_id = related_entity_id
        self.related_entity_type = related_entity_type

    def validate(self) -> Tuple[bool, Optional[str]]:
        """
        Validate notification.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.message or len(self.message.strip()) < 3:
            return False, "Message must be at least 3 characters"

        if not isinstance(self.user_id, int) or self.user_id <= 0:
            return False, "Invalid user_id"

        if not isinstance(self.notification_type, NotificationType):
            return False, "Invalid notification type"

        return True, None

    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self.status = NotificationStatus.READ
        self.updated_at = datetime.now()

    def archive(self) -> None:
        """Archive notification."""
        self.status = NotificationStatus.ARCHIVED
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.

        Follows consistent serialization format like Task, Project, Category, Tag.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "notification_type": self.notification_type.value,
            "status": self.status.value,
            "related_entity_id": self.related_entity_id,
            "related_entity_type": self.related_entity_type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Notification(id={self.id}, user_id={self.user_id}, "
            f"type={self.notification_type.value}, status={self.status.value})"
        )
