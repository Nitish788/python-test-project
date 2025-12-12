"""Base validator class and validation utilities."""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any, List
import re


class BaseValidator(ABC):
    """Abstract base class for validators."""

    @abstractmethod
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a value.

        Args:
            value: Value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        pass


class StringLengthValidator(BaseValidator):
    """Validator for string length."""

    def __init__(self, min_length: int = 0, max_length: int = 255) -> None:
        """Initialize StringLengthValidator."""
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate string length."""
        if not isinstance(value, str):
            return False, "Value must be a string"

        if len(value) < self.min_length:
            return False, f"Must be at least {self.min_length} characters"

        if len(value) > self.max_length:
            return False, f"Cannot exceed {self.max_length} characters"

        return True, None


class EmailValidator(BaseValidator):
    """Validator for email addresses."""

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate email address."""
        if not isinstance(value, str):
            return False, "Email must be a string"

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            return False, "Invalid email format"

        return True, None


class StatusValidator(BaseValidator):
    """Validator for predefined status values."""

    def __init__(self, valid_statuses: List[str]) -> None:
        """Initialize StatusValidator."""
        self.valid_statuses = valid_statuses

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate status."""
        if value not in self.valid_statuses:
            return False, f"Status must be one of: {', '.join(self.valid_statuses)}"

        return True, None
