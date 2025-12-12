"""Base classes for models and repositories."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from datetime import datetime
from app.common.exceptions import NotFoundError

T = TypeVar("T")


class BaseModel(ABC):
    """Abstract base class for all models."""

    def __init__(self, model_id: int, created_at: Optional[datetime] = None) -> None:
        """
        Initialize BaseModel.

        Args:
            model_id: Unique identifier
            created_at: Creation timestamp
        """
        self.id = model_id
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        pass

    @abstractmethod
    def validate(self) -> Tuple[bool, Optional[str]]:
        """
        Validate the model.

        Returns:
            Tuple of (is_valid, error_message)
        """
        pass

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(id={self.id})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, BaseModel):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)


class BaseRepository(Generic[T], ABC):
    """Abstract base class for repositories."""

    def __init__(self) -> None:
        """Initialize repository."""
        self._items: Dict[int, T] = {}
        self._next_id = 1

    @abstractmethod
    def create(self, **kwargs: Any) -> T:
        """Create a new item."""
        pass

    def get(self, item_id: int) -> Optional[T]:
        """
        Get item by ID.

        Args:
            item_id: Item ID

        Returns:
            Item or None if not found
        """
        return self._items.get(item_id)

    def get_or_raise(self, item_id: int, resource_type: str = "Item") -> T:
        """
        Get item by ID or raise NotFoundError.

        Args:
            item_id: Item ID
            resource_type: Type of resource for error message

        Returns:
            Item

        Raises:
            NotFoundError: If item not found
        """
        item = self.get(item_id)
        if not item:
            raise NotFoundError(f"{resource_type} not found", resource_type)
        return item

    def get_all(self) -> List[T]:
        """Get all items."""
        return list(self._items.values())

    def update(self, item_id: int, item: T) -> bool:
        """
        Update item by ID.

        Args:
            item_id: Item ID
            item: Updated item

        Returns:
            True if updated, False if not found
        """
        if item_id in self._items:
            self._items[item_id] = item
            return True
        return False

    def delete(self, item_id: int) -> bool:
        """
        Delete item by ID.

        Args:
            item_id: Item ID

        Returns:
            True if deleted, False if not found
        """
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

    def count(self) -> int:
        """Get total number of items."""
        return len(self._items)

    def exists(self, item_id: int) -> bool:
        """Check if item exists."""
        return item_id in self._items

    def get_next_id(self) -> int:
        """Get next ID and increment counter."""
        current_id = self._next_id
        self._next_id += 1
        return current_id


from typing import Tuple
