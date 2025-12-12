"""Tag model - demonstrates BaseModel usage."""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from app.common.base import BaseModel


class Tag(BaseModel):
    """
    Tag model.

    Demonstrates lightweight BaseModel implementation
    for tagging system.
    """

    def __init__(
        self,
        tag_id: int,
        name: str,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialize Tag."""
        super().__init__(tag_id, created_at)
        self.name = name
        self.usage_count = 0

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate tag."""
        if not self.name or len(self.name.strip()) == 0:
            return False, "Tag name is required"

        if len(self.name) > 30:
            return False, "Tag name cannot exceed 30 characters"

        if not self.name.isalnum():
            return False, "Tag name must be alphanumeric"

        return True, None

    def increment_usage(self) -> None:
        """Increment usage count."""
        self.usage_count += 1
        self.updated_at = datetime.now()

    def decrement_usage(self) -> None:
        """Decrement usage count."""
        if self.usage_count > 0:
            self.usage_count -= 1
            self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"Tag(id={self.id}, name='{self.name}')"
