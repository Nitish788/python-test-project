"""Common exception classes used throughout the application."""

from typing import Optional, Dict, Any


class AppException(Exception):
    """Base exception for the application."""

    def __init__(
        self,
        message: str,
        error_code: str = "APP_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize AppException.

        Args:
            message: Exception message
            error_code: Error code identifier
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(AppException):
    """Raised when validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize ValidationError."""
        super().__init__(message, "VALIDATION_ERROR", details)


class NotFoundError(AppException):
    """Raised when a resource is not found."""

    def __init__(self, message: str, resource_type: str = "Resource") -> None:
        """Initialize NotFoundError."""
        super().__init__(
            message,
            "NOT_FOUND",
            {"resource_type": resource_type},
        )


class ConflictError(AppException):
    """Raised when there's a conflict (e.g., duplicate)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize ConflictError."""
        super().__init__(message, "CONFLICT", details)


class PermissionError(AppException):
    """Raised when user lacks permission."""

    def __init__(self, message: str = "Permission denied") -> None:
        """Initialize PermissionError."""
        super().__init__(message, "PERMISSION_DENIED")
