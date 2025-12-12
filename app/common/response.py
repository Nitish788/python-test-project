"""Response models for consistent API responses."""

from typing import Any, Dict, Optional, Generic, TypeVar
from enum import Enum
from datetime import datetime

T = TypeVar("T")


class ResponseStatus(Enum):
    """Response status enumeration."""

    SUCCESS = "success"
    ERROR = "error"
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class ResponseModel(Generic[T]):
    """Generic response model for consistent API responses."""

    def __init__(
        self,
        status: ResponseStatus,
        data: Optional[T] = None,
        message: str = "",
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Initialize ResponseModel.

        Args:
            status: Response status
            data: Response data
            message: Response message
            timestamp: Timestamp of response
        """
        self.status = status
        self.data = data
        self.message = message
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "status": self.status.value,
            "data": self.data,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
        }


class SuccessResponse(ResponseModel[T]):
    """Success response helper."""

    def __init__(self, data: Optional[T] = None, message: str = "Success") -> None:
        """Initialize SuccessResponse."""
        super().__init__(ResponseStatus.SUCCESS, data, message)


class ErrorResponse(ResponseModel[None]):
    """Error response helper."""

    def __init__(self, message: str, error_code: str = "ERROR") -> None:
        """Initialize ErrorResponse."""
        super().__init__(ResponseStatus.ERROR, None, message)
        self.error_code = error_code

    def to_dict(self) -> Dict[str, Any]:
        """Convert error response to dictionary."""
        response = super().to_dict()
        response["error_code"] = self.error_code
        return response
