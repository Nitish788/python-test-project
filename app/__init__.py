"""
TODO Management Application
A comprehensive task management system demonstrating shared components
and reusable patterns across multiple entities.
"""

from app.common.base import BaseModel, BaseRepository
from app.common.exceptions import (
    AppException,
    ValidationError,
    NotFoundError,
    ConflictError,
)
from app.common.interfaces import (
    IModel,
    IRepository,
    IValidator,
    IService,
    INotificationService,
)
from app.constants import (
    # Status constants
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_ARCHIVED,
    TASK_STATUSES,
    TASK_PRIORITY_LOW,
    TASK_PRIORITY_MEDIUM,
    TASK_PRIORITY_HIGH,
    TASK_PRIORITY_CRITICAL,
    TASK_PRIORITIES,
    PROJECT_STATUSES,
    NOTIFICATION_STATUSES,
    NOTIFICATION_TYPES,
    # Validation constants
    TASK_TITLE_MIN_LENGTH,
    TASK_TITLE_MAX_LENGTH,
    TASK_DESCRIPTION_MAX_LENGTH,
    # Color constants
    DEFAULT_CATEGORY_COLORS,
    # Error messages
    ERROR_INVALID_EMAIL,
    ERROR_TASK_NOT_FOUND,
    ERROR_DUPLICATE_TAG,
    # Success messages
    SUCCESS_TASK_CREATED,
    # App config
    APP_NAME,
    APP_VERSION,
)

__version__ = "1.0.0"
__author__ = "TODO App Team"

__all__ = [
    # Base classes
    "BaseModel",
    "BaseRepository",
    # Exceptions
    "AppException",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    # Interfaces
    "IModel",
    "IRepository",
    "IValidator",
    "IService",
    "INotificationService",
    # Status constants
    "TASK_STATUS_PENDING",
    "TASK_STATUS_IN_PROGRESS",
    "TASK_STATUS_COMPLETED",
    "TASK_STATUS_ARCHIVED",
    "TASK_STATUSES",
    "TASK_PRIORITY_LOW",
    "TASK_PRIORITY_MEDIUM",
    "TASK_PRIORITY_HIGH",
    "TASK_PRIORITY_CRITICAL",
    "TASK_PRIORITIES",
    "PROJECT_STATUSES",
    "NOTIFICATION_STATUSES",
    "NOTIFICATION_TYPES",
    # Validation constants
    "TASK_TITLE_MIN_LENGTH",
    "TASK_TITLE_MAX_LENGTH",
    "TASK_DESCRIPTION_MAX_LENGTH",
    # Color constants
    "DEFAULT_CATEGORY_COLORS",
    # Error messages
    "ERROR_INVALID_EMAIL",
    "ERROR_TASK_NOT_FOUND",
    "ERROR_DUPLICATE_TAG",
    # Success messages
    "SUCCESS_TASK_CREATED",
    # App config
    "APP_NAME",
    "APP_VERSION",
]
