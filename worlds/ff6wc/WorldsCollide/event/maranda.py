from ..event.event import *

class Maranda(Event):
    def name(self):
        return "Maranda"

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(npc_bit.MAN_CENTER_MARANDA),
            field.ClearEventBit(npc_bit.SOLDIERS_MARANDA),
        )

    def mod(self):
        pass
