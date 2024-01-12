from enum import IntEnum
from datetime import datetime
import threading
import time
import os
import json
import sys
import asyncio
import shutil
import logging
import re

#type of message that should be sent to the game
class KH1_message_type(IntEnum):
    invalid       = -1
    test          = 0
    recieved_trap = 1
    sent_item     = 2
    deathlink     = 3
    player_joined = 4
    player_left   = 5


#non-persistent message that is sent to the game
class KH1_UniversalMessage():
    def __init__(self, type : KH1_message_type , values : list[str]):
        self.type: KH1_message_type = type
        self.values: list[str] = values

    def as_message(self):
        as_string = str(self.type.value) + "\n"
        for value in self.values:
            as_string += value + "\n"
        return as_string

class KH1_MessageHandler():
    def __init__(self, intervalSeconds: int, directory: str):
        self.interval = intervalSeconds
        self.directory = directory
        self.message_cache : list[KH1_UniversalMessage] = []
        self.timer = threading.Timer(self.interval, self.send_messages)
        self.timer.start()

    def receive_message(self, type: KH1_message_type, values: list[str]):
        new_message = KH1_UniversalMessage(type, values)
        self.message_cache.append(new_message)

    def send_messages(self):
        valid_messages = []
        for message in self.message_cache:
            if message.type != KH1_message_type.invalid:
                valid_messages.append(message)

        if len(valid_messages) > 0:
            print("Sending messages to KH1")
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            all_messages: str = ""
            all_messages += current_time + "\n"

            for message in valid_messages:
                all_messages += message.as_message()
                all_messages += "-\n"

            with open(os.path.join(self.directory, "messages.sem"), 'w') as f:
                f.write(all_messages)
                f.close()

            os.rename(
                os.path.join(self.directory, "messages.sem"),
                os.path.join(self.directory, "messages")
            )

        self.message_cache.clear()
        self.timer = threading.Timer(self.interval, self.send_messages)
        self.timer.start()


    def stop_sending(self):
        self.timer.cancel()
