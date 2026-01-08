import time
from typing import Callable, List


class NotificationManager:
    notification_queue: List[str] = []
    time_since_last_message: float = 0
    last_message_time: float = 0
    message_duration: float
    send_notification_func: Callable[[str], bool]

    def __init__(
        self, message_duration: float, send_notification_func: Callable[[str], bool]
    ):
        self.message_duration = (
            message_duration / 2
        )  # If there are multiple messages, the duration is shorter
        self.send_notification_func = send_notification_func

    def queue_notification(self, message: str):
        self.notification_queue.append(message)

    def handle_notifications(self):
        self.time_since_last_message = time.time() - self.last_message_time
        if (
            len(self.notification_queue) > 0
            and self.time_since_last_message >= self.message_duration
        ):
            notification = self.notification_queue[0]
            result = self.send_notification_func(notification)
            if result:
                self.notification_queue.pop(0)
                self.last_message_time = time.time()
                self.time_since_last_message = 0
