from typing import Dict, List, Optional
from app.models.notification import Notification, NotificationStatus
from app.common.base import BaseRepository
import logging

logger = logging.getLogger(__name__)

class AlertRepository(BaseRepository[Notification]):
    
    def create(self, notification: Notification) -> Notification:
        logger.info(f"Creating alert: {notification.message}")
        self._storage[notification._id] = notification
        return notification