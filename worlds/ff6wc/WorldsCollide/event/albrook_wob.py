from ..event.event import *

class AlbrookWOB(Event):
    def name(self):
        return "Albrook WOB"

    def init_event_bits(self, space):
        space.write(
            field.ClearEventBit(npc_bit.GENERAL_LEO_SOLDIERS_ALBROOK_PORT),
        )

    def mod(self):
        space = Reserve(0xc62f2, 0xc62f7, "albrook block port west if banquet dinner finished", field.NOP())
        space = Reserve(0xc632d, 0xc6332, "albrook block port east if banquet dinner finished", field.NOP())

        self.inn_locke_celes_event_mod()

    def inn_locke_celes_event_mod(self):
        space = Reserve(0xc614a, 0xc614f, "albrook locke/celes scene condition", field.NOP())
        space.write(
            field.Branch(0xc62a6),
        )
