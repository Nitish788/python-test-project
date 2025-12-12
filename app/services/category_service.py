"""Category service - demonstrates BaseRepository usage."""

from typing import List
from app.common.base import BaseRepository
from app.common.exceptions import ValidationError
from app.models.category import Category
import logging

logger = logging.getLogger(__name__)


class CategoryRepository(BaseRepository[Category]):
    """Repository for managing categories."""

    def create(
        self,
        name: str,
        color: str = "#000000",
        description: str = "",
    ) -> Category:
        """
        Create a new category.

        Args:
            name: Category name
            color: Category color (hex)
            description: Category description

        Returns:
            Created category

        Raises:
            ValidationError: If category data is invalid
        """
        category = Category(
            category_id=self.get_next_id(),
            name=name,
            color=color,
            description=description,
        )

        # Validate before storing
        is_valid, error = category.validate()
        if not is_valid:
            raise ValidationError(error)

        # Check for duplicate names
        for cat in self._items.values():
            if cat.name.lower() == name.lower():
                raise ValidationError(f"Category '{name}' already exists")

        self._items[category.id] = category
        logger.info(f"Category created: {category}")
        return category

    def find_by_name(self, name: str) -> List[Category]:
        """Find categories by name (case-insensitive)."""
        name_lower = name.lower()
        return [c for c in self._items.values() if name_lower in c.name.lower()]

    def get_by_name(self, name: str) -> Category:
        """Get category by exact name."""
        for cat in self._items.values():
            if cat.name.lower() == name.lower():
                return cat
        raise ValueError(f"Category '{name}' not found")
