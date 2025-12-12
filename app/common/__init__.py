"""Common/shared components used across the application."""

from app.common.base import BaseModel, BaseRepository
from app.common.response import ResponseModel, ErrorResponse, SuccessResponse
from app.common.validators import BaseValidator
from app.common.exceptions import AppException, ValidationError, NotFoundError, ConflictError
from app.common.interfaces import (
    IModel,
    IRepository,
    IValidator,
    IService,
    INotificationService,
)

__all__ = [
    # Base classes
    "BaseModel",
    "BaseRepository",
    # Response models
    "ResponseModel",
    "ErrorResponse",
    "SuccessResponse",
    # Validators
    "BaseValidator",
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
]
