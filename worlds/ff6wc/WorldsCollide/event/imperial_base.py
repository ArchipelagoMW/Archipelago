from ..event.event import *

class ImperialBase(Event):
    def name(self):
        return "Imperial Base"

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.ESPERS_CRASHED_AIRSHIP), # allow entrance without terra in party
            field.ClearEventBit(npc_bit.TREASURE_ROOM_DOOR_IMPERIAL_BASE),
        )

    def mod(self):
        self.entrance_event_mod()

    def entrance_event_mod(self):
        SOLDIERS_BATTLE_ON_TOUCH = 0xb25b9

        space = Reserve(0xb25d6, 0xb25f8, "imperial base entrance event conditions", field.NOP())
        if self.args.character_gating:
            space.write(
                #field.BranchIfEventBitSet(event_bit.character_recruited(self.events["Sealed Gate"].character_gate()), SOLDIERS_BATTLE_ON_TOUCH),
                field.ReturnIfEventBitSet(event_bit.character_recruited(self.events["Sealed Gate"].character_gate())),
            )
        else:
            space.write(
                #field.Branch(SOLDIERS_BATTLE_ON_TOUCH),
                field.Return(),
            )
