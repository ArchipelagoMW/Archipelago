from ..event.event import *

class DuncanHouseWOR(Event):
    def name(self):
        return "Duncan House WOR"

    def init_event_bits(self, space):
        if not self.args.bum_rush_last:
            space.write(
                field.SetEventBit(event_bit.CAN_LEARN_BUM_RUSH),
            )

    def mod(self):
        self.bum_rush_dialog_mod()
        self.bum_rush_learn_mod()
        if self.args.flashes_remove_most or self.args.flashes_remove_worst:
            self.bum_rush_flash_mod()

    def bum_rush_dialog_mod(self):
        space = Reserve(0xc0c25, 0xc0c27, "duncan house wor duncan!!", field.NOP())
        space = Reserve(0xc0c54, 0xc0c56, "duncan house wor why the surprised face", field.NOP())
        space = Reserve(0xc0c5e, 0xc0c60, "duncan house wor i'm so glad you're safe", field.NOP())
        space = Reserve(0xc0c8e, 0xc0c90, "duncan house wor tears??", field.NOP())
        space = Reserve(0xc0ccd, 0xc0ccf, "duncan house wor earth yawned", field.NOP())
        space = Reserve(0xc0ce0, 0xc0ce2, "duncan house wor time to complete your training", field.NOP())
        space = Reserve(0xc0cf0, 0xc0cf2, "duncan house wor put 'em up", field.NOP())
        space = Reserve(0xc0ec8, 0xc0eca, "duncan house wor the bum rush", field.NOP())
        space = Reserve(0xc0ede, 0xc0ee0, "duncan house wor give kefka the boot", field.NOP())

    def bum_rush_learn_mod(self):
        space = Reserve(0xc0bd8, 0xc0be4, "duncan house bum rush return if sabin not in party", field.NOP())
        space.write(
            field.ReturnIfEventBitClear(event_bit.CAN_LEARN_BUM_RUSH),
            field.ReturnIfEventBitSet(event_bit.LEARNED_BUM_RUSH),
        )

        # if sabin in party, learn it with him, otherwise, learn with lowest character id in party
        src = [
            field.ReturnIfCharacterNotInParty(self.characters.SABIN),
            Read(0xc0c05, 0xc0c09),  # set sabin as party leader
            field.Return(),
        ]
        space = Write(Bank.CB, src, "duncan house bum rush make sabin leader if in party")
        choose_leader = space.start_address

        space = Reserve(0xc0c05, 0xc0c09, "duncan house bum rush set sabin as party leader", field.NOP())
        space.write(
            field.Call(choose_leader),
        )

        # change sabin to party leader
        sabin_action_queues = [0xc0c1c, 0xc0c37, 0xc0c58, 0xc0cac, 0xc0cd8, 0xc0ce8, 0xc0cf5, 0xc0d2b, 0xc0d35,
                               0xc0d40, 0xc0d4e, 0xc0d71, 0xc0d91, 0xc0db1, 0xc0dc4, 0xc0dcc, 0xc0dd4, 0xc0de7,
                               0xc0e01, 0xc0e1a, 0xc0e33, 0xc0e58, 0xc0e6b, 0xc0e6f, 0xc0e86, 0xc0e9e, 0xc0ebf,
                               0xc0ecc, 0xc0eee, 0xc0eff, 0xc0f09, 0xc0f30, 0xc0f43, 0xc0f47]
        for address in sabin_action_queues:
            space = Reserve(address, address, "duncan house learn bum rush sabin")
            space.write(field_entity.PARTY0)

    def bum_rush_flash_mod(self):
        flash_addresses = [0xc0d12, 0xc0d5f, 0xc0d7f, 0xc0d9f, 0xc0df0, 0xc0e09, 0xc0e22, 0xc0e3b, 0xc0e65, 0xc0e74]
        for address in flash_addresses:
            space = Reserve(address, address + 1, "duncan house wor bum rush flash", field.FlashScreen(field.Flash.NONE))