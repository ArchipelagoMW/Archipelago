from ..event.event import *

class Coliseum(Event):
    def name(self):
        return "Coliseum"

    def mod(self):
        self.after_coliseum_battle_mod()
        self.recruit_shadow_mod()
        self.npc_shadow_dialog_mod()

    def after_coliseum_battle_mod(self):
        src = [
            Read(0xb796d, 0xb7970), # call function to unfade screen

            field.BranchIfBattleEventBitClear(battle_bit.PARTY_ANNIHILATED, "VICTORY"),
            field.Return(),

            "VICTORY",
            field.SetEventBit(event_bit.WON_A_COLISEUM_MATCH),
            field.CheckObjectives(),
            field.Return(),
        ]
        space = Write(Bank.CB, src, "coliseum after battle")
        after_battle = space.start_address

        space = Reserve(0xb796d, 0xb7970, "coliseum call after battle")
        space.write(
            field.Call(after_battle),
        )

    def recruit_shadow_mod(self):
        invoke_coliseum_battle = 0xb796c

        space = Reserve(0xb78e3, 0xb78e9, "coliseum recruit shadow check", field.NOP())
        space.write(
            field.Branch(invoke_coliseum_battle),
            field.Return(),
        )
        Free(0xb78ea, 0xb796b) # recruit shadow event

    def npc_shadow_dialog_mod(self):
        # remove shadow available dialog from npc sitting at table
        space = Reserve(0xb78ad, 0xb78b5, "coliseum npc shadow striker dialog", field.NOP())
        space.write(
            field.Branch(0xb78a9),
        )
