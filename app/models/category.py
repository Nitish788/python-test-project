"""Category model - demonstrates BaseModel usage."""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from app.common.base import BaseModel


class Category(BaseModel):
    """
    Category model.

    Demonstrates simpler BaseModel implementation
    for organizing tasks.
    """

    def __init__(
        self,
        category_id: int,
        name: str,
        color: str = "#000000",
        description: str = "",
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialize Category."""
        super().__init__(category_id, created_at)
        self.name = name
        self.color = color
        self.description = description
        self.task_count = 0

    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate category."""
        if not self.name or len(self.name.strip()) == 0:
            return False, "Category name is required"

        if len(self.name) > 50:
            return False, "Category name cannot exceed 50 characters"

        if not self._is_valid_hex_color(self.color):
            return False, "Invalid hex color format"

        return True, None

    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """Validate hex color."""
        if not color.startswith("#"):
            return False
        hex_part = color[1:]
        return len(hex_part) == 6 and all(c in "0123456789abcdefABCDEF" for c in hex_part)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "description": self.description,
            "task_count": self.task_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"Category(id={self.id}, name='{self.name}')"
