from ..event.event import *

class DuncanHouseWOB(Event):
    def name(self):
        return "Duncan House WOB"

    def init_event_bits(self, space):
        pass

    def mod(self):
        # favorite flowers
        self.maps.delete_event(0x05e, 81, 35)

        # favorite tea
        self.maps.delete_event(0x05e, 75, 28)

        # favorite dishes
        self.maps.delete_event(0x05e, 78, 29)
        self.maps.delete_event(0x05e, 79, 29)

        # entrance event
        self.maps.delete_event(0x05e, 80, 36)
