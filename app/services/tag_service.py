"""Tag service - demonstrates BaseRepository usage."""

from typing import List
from app.common.base import BaseRepository
from app.common.exceptions import ValidationError
from app.models.tag import Tag
import logging

logger = logging.getLogger(__name__)


class TagRepository(BaseRepository[Tag]):
    """Repository for managing tags."""

    def create(self, name: str) -> Tag:
        """
        Create a new tag.

        Args:
            name: Tag name

        Returns:
            Created tag

        Raises:
            ValidationError: If tag data is invalid
        """
        tag = Tag(
            tag_id=self.get_next_id(),
            name=name,
        )

        # Validate before storing
        is_valid, error = tag.validate()
        if not is_valid:
            raise ValidationError(error)

        # Check for duplicates
        for existing_tag in self._items.values():
            if existing_tag.name.lower() == name.lower():
                raise ValidationError(f"Tag '{name}' already exists")

        self._items[tag.id] = tag
        logger.info(f"Tag created: {tag}")
        return tag

    def find_by_name(self, name: str) -> List[Tag]:
        """Find tags by name."""
        name_lower = name.lower()
        return [t for t in self._items.values() if name_lower in t.name.lower()]

    def get_by_name(self, name: str) -> Tag:
        """Get tag by exact name."""
        for tag in self._items.values():
            if tag.name.lower() == name.lower():
                return tag
        raise ValueError(f"Tag '{name}' not found")

    def get_popular_tags(self, limit: int = 10) -> List[Tag]:
        """Get most used tags."""
        sorted_tags = sorted(
            self._items.values(),
            key=lambda t: t.usage_count,
            reverse=True,
        )
        return sorted_tags[:limit]
