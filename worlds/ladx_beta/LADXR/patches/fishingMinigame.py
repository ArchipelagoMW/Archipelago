from ..assembler import ASM
from ..roomEditor import RoomEditor


def updateFinishingMinigame(rom):
    rom.patch(0x04, 0x26BE, 0x26DF, ASM("""
        ld   a, $0E ; GiveItemAndMessageForRoomMultiworld
        rst  8
        
        ; Mark selection as stopping minigame, as we are not asking a question.
        ld   a, $01
        ld   [$C177], a
        
        ; Check if we got rupees from the item skip getting rupees from the fish.
        ld   a, [$DB90]
        ld   hl, $DB8F
        or   [hl]
        jp   nz, $66FE
    """), fill_nop=True)
