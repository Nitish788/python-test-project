"""
Interface definitions for the TODO application.
These define contracts that all implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Generic

T = TypeVar('T')


class IModel(ABC):
    """Interface that all models must implement."""
    
    @property
    @abstractmethod
    def id(self) -> int:
        """Unique identifier for the model."""
        pass
    
    @abstractmethod
    def validate(self) -> Tuple[bool, Optional[str]]:
        """
        Validate the model.
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize model to dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        pass


class IRepository(ABC, Generic[T]):
    """Interface that all repositories must implement."""
    
    @abstractmethod
    def create(self, **kwargs) -> T:
        """
        Create a new entity.
        
        Raises:
            ValidationError: If validation fails
        
        Returns:
            T: The created entity
        """
        pass
    
    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """
        Get entity by id.
        
        Args:
            id: Entity identifier
        
        Returns:
            Optional[T]: Entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Get all entities.
        
        Returns:
            List[T]: List of all entities
        """
        pass
    
    @abstractmethod
    def update(self, id: int, entity: T) -> T:
        """
        Update an entity.
        
        Args:
            id: Entity identifier
            entity: Updated entity
        
        Raises:
            NotFoundError: If entity not found
        
        Returns:
            T: Updated entity
        """
        pass
    
    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Delete an entity.
        
        Args:
            id: Entity identifier
        
        Raises:
            NotFoundError: If entity not found
        """
        pass


class IValidator(ABC):
    """Interface for all validators."""
    
    @abstractmethod
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a value.
        
        Args:
            value: Value to validate
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        pass


class IService(ABC):
    """Interface for business logic services."""
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Execute service logic.
        
        Returns:
            Any: Service result
        """
        pass


class INotificationService(ABC):
    """Interface for notification services."""
    
    @abstractmethod
    def send(self, message: str, recipient_id: int) -> bool:
        """
        Send a notification.
        
        Args:
            message: Notification message
            recipient_id: Recipient user id
        
        Returns:
            bool: True if sent successfully
        """
        pass
    
    @abstractmethod
    def notify_task_assigned(self, task_id: int, assignee_id: int) -> bool:
        """Send task assigned notification."""
        pass
    
    @abstractmethod
    def notify_task_due_soon(self, task_id: int, user_id: int) -> bool:
        """Send task due soon notification."""
        pass
    
    @abstractmethod
    def notify_task_completed(self, task_id: int, user_id: int) -> bool:
        """Send task completed notification."""
        pass
