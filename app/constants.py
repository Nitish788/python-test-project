"""
Application-wide constants.
Module-level constants in UPPER_CASE as per Python conventions.
"""

from typing import TypeAlias

# ============================================================================
# STATUS CONSTANTS
# ============================================================================

# Task Statuses
TASK_STATUS_PENDING: str = "pending"
TASK_STATUS_IN_PROGRESS: str = "in_progress"
TASK_STATUS_COMPLETED: str = "completed"
TASK_STATUS_ARCHIVED: str = "archived"

TASK_STATUSES: list[str] = [
    TASK_STATUS_PENDING,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_ARCHIVED,
]

# Task Priorities
TASK_PRIORITY_LOW: str = "low"
TASK_PRIORITY_MEDIUM: str = "medium"
TASK_PRIORITY_HIGH: str = "high"
TASK_PRIORITY_CRITICAL: str = "critical"

TASK_PRIORITIES: list[str] = [
    TASK_PRIORITY_LOW,
    TASK_PRIORITY_MEDIUM,
    TASK_PRIORITY_HIGH,
    TASK_PRIORITY_CRITICAL,
]

# Project Statuses
PROJECT_STATUS_PLANNING: str = "planning"
PROJECT_STATUS_ACTIVE: str = "active"
PROJECT_STATUS_ON_HOLD: str = "on_hold"
PROJECT_STATUS_COMPLETED: str = "completed"
PROJECT_STATUS_ARCHIVED: str = "archived"

PROJECT_STATUSES: list[str] = [
    PROJECT_STATUS_PLANNING,
    PROJECT_STATUS_ACTIVE,
    PROJECT_STATUS_ON_HOLD,
    PROJECT_STATUS_COMPLETED,
    PROJECT_STATUS_ARCHIVED,
]

# Notification Statuses
NOTIFICATION_STATUS_UNREAD: str = "unread"
NOTIFICATION_STATUS_READ: str = "read"
NOTIFICATION_STATUS_ARCHIVED: str = "archived"

NOTIFICATION_STATUSES: list[str] = [
    NOTIFICATION_STATUS_UNREAD,
    NOTIFICATION_STATUS_READ,
    NOTIFICATION_STATUS_ARCHIVED,
]

# Notification Types
NOTIFICATION_TYPE_TASK_ASSIGNED: str = "task_assigned"
NOTIFICATION_TYPE_TASK_COMPLETED: str = "task_completed"
NOTIFICATION_TYPE_TASK_DUE_SOON: str = "task_due_soon"
NOTIFICATION_TYPE_PROJECT_UPDATED: str = "project_updated"
NOTIFICATION_TYPE_COMMENT_ADDED: str = "comment_added"

NOTIFICATION_TYPES: list[str] = [
    NOTIFICATION_TYPE_TASK_ASSIGNED,
    NOTIFICATION_TYPE_TASK_COMPLETED,
    NOTIFICATION_TYPE_TASK_DUE_SOON,
    NOTIFICATION_TYPE_PROJECT_UPDATED,
    NOTIFICATION_TYPE_COMMENT_ADDED,
]

# ============================================================================
# VALIDATION CONSTRAINTS
# ============================================================================

# Task Validation
TASK_TITLE_MIN_LENGTH: int = 3
TASK_TITLE_MAX_LENGTH: int = 200
TASK_DESCRIPTION_MIN_LENGTH: int = 0
TASK_DESCRIPTION_MAX_LENGTH: int = 5000

# Project Validation
PROJECT_NAME_MIN_LENGTH: int = 3
PROJECT_NAME_MAX_LENGTH: int = 100
PROJECT_DESCRIPTION_MIN_LENGTH: int = 0
PROJECT_DESCRIPTION_MAX_LENGTH: int = 5000

# Category Validation
CATEGORY_NAME_MIN_LENGTH: int = 2
CATEGORY_NAME_MAX_LENGTH: int = 50

# Tag Validation
TAG_NAME_MIN_LENGTH: int = 2
TAG_NAME_MAX_LENGTH: int = 50

# Notification Validation
NOTIFICATION_MESSAGE_MIN_LENGTH: int = 3
NOTIFICATION_MESSAGE_MAX_LENGTH: int = 500

# General Validation
EMAIL_MIN_LENGTH: int = 5
EMAIL_MAX_LENGTH: int = 255
NAME_MIN_LENGTH: int = 2
NAME_MAX_LENGTH: int = 100

# ============================================================================
# COLOR CONSTANTS
# ============================================================================

# Predefined Category Colors (Hex format)
COLOR_RED: str = "#FF5733"
COLOR_BLUE: str = "#0066FF"
COLOR_GREEN: str = "#00CC66"
COLOR_YELLOW: str = "#FFCC00"
COLOR_PURPLE: str = "#9933FF"
COLOR_ORANGE: str = "#FF9900"
COLOR_PINK: str = "#FF66CC"
COLOR_CYAN: str = "#00CCFF"

DEFAULT_CATEGORY_COLORS: list[str] = [
    COLOR_RED,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_PURPLE,
    COLOR_ORANGE,
    COLOR_PINK,
    COLOR_CYAN,
]

# ============================================================================
# PAGINATION & LIMITS
# ============================================================================

DEFAULT_PAGE_SIZE: int = 10
MAX_PAGE_SIZE: int = 100
MIN_PAGE_SIZE: int = 1

DEFAULT_LIMIT: int = 50
MAX_LIMIT: int = 1000

# ============================================================================
# TIME CONSTANTS
# ============================================================================

# Time deltas (in days)
TASK_DUE_SOON_DAYS: int = 3
NOTIFICATION_RETENTION_DAYS: int = 30
ARCHIVED_ITEM_RETENTION_DAYS: int = 90

# ============================================================================
# ERROR MESSAGES
# ============================================================================

# Validation Errors
ERROR_INVALID_EMAIL: str = "Invalid email format"
ERROR_INVALID_NAME: str = "Name is required and must be 2-100 characters"
ERROR_INVALID_COLOR: str = "Invalid hex color format (e.g., #FF5733)"
ERROR_INVALID_PRIORITY: str = f"Priority must be one of: {', '.join(TASK_PRIORITIES)}"
ERROR_INVALID_STATUS: str = f"Status must be one of: {', '.join(TASK_STATUSES)}"

# Not Found Errors
ERROR_TASK_NOT_FOUND: str = "Task not found"
ERROR_PROJECT_NOT_FOUND: str = "Project not found"
ERROR_CATEGORY_NOT_FOUND: str = "Category not found"
ERROR_TAG_NOT_FOUND: str = "Tag not found"
ERROR_NOTIFICATION_NOT_FOUND: str = "Notification not found"

# Conflict Errors
ERROR_DUPLICATE_TAG: str = "Tag with this name already exists"
ERROR_DUPLICATE_CATEGORY: str = "Category with this name already exists"

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_TASK_CREATED: str = "Task created successfully"
SUCCESS_TASK_UPDATED: str = "Task updated successfully"
SUCCESS_TASK_DELETED: str = "Task deleted successfully"

SUCCESS_PROJECT_CREATED: str = "Project created successfully"
SUCCESS_PROJECT_UPDATED: str = "Project updated successfully"
SUCCESS_PROJECT_DELETED: str = "Project deleted successfully"

SUCCESS_NOTIFICATION_SENT: str = "Notification sent successfully"

# ============================================================================
# API RESPONSE CODES
# ============================================================================

HTTP_OK: int = 200
HTTP_CREATED: int = 201
HTTP_BAD_REQUEST: int = 400
HTTP_UNAUTHORIZED: int = 401
HTTP_FORBIDDEN: int = 403
HTTP_NOT_FOUND: int = 404
HTTP_CONFLICT: int = 409
HTTP_INTERNAL_ERROR: int = 500

# ============================================================================
# TYPE ALIASES
# ============================================================================

# Type aliases for better code readability
TaskID: TypeAlias = int
ProjectID: TypeAlias = int
CategoryID: TypeAlias = int
TagID: TypeAlias = int
NotificationID: TypeAlias = int
UserID: TypeAlias = int

# ============================================================================
# DEFAULT VALUES
# ============================================================================

DEFAULT_TASK_PRIORITY: str = TASK_PRIORITY_MEDIUM
DEFAULT_TASK_STATUS: str = TASK_STATUS_PENDING
DEFAULT_PROJECT_STATUS: str = PROJECT_STATUS_ACTIVE
DEFAULT_NOTIFICATION_STATUS: str = NOTIFICATION_STATUS_UNREAD

# ============================================================================
# APPLICATION CONFIG
# ============================================================================

APP_NAME: str = "TODO Management System"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = "A comprehensive TODO management application with task assignment and notifications"

# Debug mode
DEBUG_MODE: bool = False
VERBOSE_LOGGING: bool = False

# ============================================================================
# DATETIME FORMATS
# ============================================================================

ISO_DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
ISO_DATE_FORMAT: str = "%Y-%m-%d"
READABLE_DATETIME_FORMAT: str = "%B %d, %Y %H:%M:%S"
