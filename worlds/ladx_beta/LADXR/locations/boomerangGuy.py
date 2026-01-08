from .itemInfo import ItemInfo
from .constants import *
from ..assembler import ASM
from ..utils import formatText


class BoomerangGuy(ItemInfo):
    OPTIONS = [BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL]

    def __init__(self):
        super().__init__(0x1F5)
        self.setting = 'trade'

    def configure(self, options):
        self.MULTIWORLD = False

        self.setting = options.boomerang
        if self.setting == 'gift':
            self.MULTIWORLD = True

    # Cannot trade:
    # SWORD, BOMB, SHIELD, POWER_BRACELET, OCARINA, MAGIC_POWDER, BOW
    # Checks for these are at $46A2, and potentially we could remove those.
    # But SHIELD, BOMB and MAGIC_POWDER would most likely break things.
    # SWORD and POWER_BRACELET would most likely introduce the lv0 shield/bracelet issue
    def patch(self, rom, option, *, multiworld=None):
        if self.setting == 'trade':
            inv = INVENTORY_MAP[option]
            # Patch the check if you traded back the boomerang (so traded twice)
            rom.patch(0x19, 0x063F, ASM("cp $0D"), ASM("cp $%s" % (inv)))
            # Item to give by "default" (aka, boomerang)
            rom.patch(0x19, 0x06C1, ASM("ld a, $0D"), ASM("ld a, $%s" % (inv)))
            # Check if inventory slot is boomerang to give back item in this slot
            rom.patch(0x19, 0x06FC, ASM("cp $0D"), ASM("cp $%s" % (inv)))
            # Put the boomerang ID in the inventory of the boomerang guy (aka, traded back)
            rom.patch(0x19, 0x0710, ASM("ld a, $0D"), ASM("ld a, $%s" % (inv)))

            rom.texts[0x222] = formatText("Okay, let's do it!")
            rom.texts[0x224] = formatText("You got the {%s} in exchange for the item you had." % (option))
            rom.texts[0x225] = formatText("Give me back my {%s}, I beg you! I'll return the item you gave me" % (option), ask="Okay Not Now")
            rom.texts[0x226] = formatText("The item came back to you. You returned the other item.")
        else:
            # Patch the inventory trade to give an specific item instead
            rom.texts[0x221] = formatText("I found a good item washed up on the beach... Want to have it?", ask="Okay No")
            rom.patch(0x19, 0x069C, 0x06C6, ASM("""
                ; Mark trade as done
                ld a, $06
                ld [$DB7D], a

                ld a, [$472B]
                ldh [$FFF1], a
                ld a, $06
                rst 8
                
                ld a, $0D
            """), fill_nop=True)
            # Show the right item above link
            rom.patch(0x19, 0x0786, 0x0793, ASM("""
                ld a, [$472B]
                ldh [$FFF1], a
                ld a, $01
                rst 8
            """), fill_nop=True)
            # Give the proper message for this item
            rom.patch(0x19, 0x075A, 0x076A, ASM("""
                ld a, [$472B]
                ldh [$FFF1], a
                ld a, $0A
                rst 8
            """), fill_nop=True)
            rom.patch(0x19, 0x072B, "00", "%02X" % (CHEST_ITEMS[option]))

            # Ignore the trade back.
            rom.texts[0x225] = formatText("It's a secret to everybody.")
            rom.patch(0x19, 0x0668, ASM("ld a, [$DB7D]"), ASM("ret"), fill_nop=True)

            if multiworld is not None:
                rom.banks[0x3E][0x3300 + self.room] = multiworld

    def read(self, rom):
        if rom.banks[0x19][0x06C5] == 0x00:
            for k, v in CHEST_ITEMS.items():
                if v == rom.banks[0x19][0x072B]:
                    return k
        else:
            for k, v in INVENTORY_MAP.items():
                if int(v, 16) == rom.banks[0x19][0x0640]:
                    return k
        raise ValueError()
