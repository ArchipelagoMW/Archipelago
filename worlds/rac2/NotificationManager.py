import time
from dataclasses import dataclass
from typing import Optional

from .Rac2Interface import Rac2Interface
from .TextManager import TextManager


@dataclass
class QueuedMessage:
    message: str
    duration: float


class NotificationManager:
    notification_queue: list[QueuedMessage] = []
    last_message_time: float = 0
    message_duration: float = None
    default_duration: float = None
    is_waiting_for_message_processing: bool = False

    def __init__(self, message_duration):
        self.message_duration = message_duration
        self.default_duration = message_duration

    def queue_size(self) -> int:
        return len(self.notification_queue)

    def queue_notification(self, message, duration: Optional[float] = None):
        self.notification_queue.append(QueuedMessage(message, duration if duration else self.message_duration))

    def has_message_to_display(self):
        if len(self.notification_queue) <= 0:
            return False
        if self.is_waiting_for_message_processing:
            return False
        return time.time() - self.last_message_time >= self.message_duration

    def handle_notifications(self, game_interface: Rac2Interface, text_manager: TextManager):
        if self.is_waiting_for_message_processing:
            if not game_interface.is_hud_notification_pending():
                self.is_waiting_for_message_processing = False
                self.last_message_time = time.time()
        elif self.has_message_to_display() and game_interface.can_display_hud_notification():
            notification = self.notification_queue.pop(0)
            self.message_duration = notification.duration
            self.is_waiting_for_message_processing = True
            text_manager.set_hud_notification_text(notification.message)
            game_interface.trigger_hud_notification_display()
