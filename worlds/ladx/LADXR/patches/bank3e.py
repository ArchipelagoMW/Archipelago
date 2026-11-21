import os
import binascii
from ..assembler import ASM
from ..utils import formatText

import pkgutil

def hasBank3E(rom):
    return rom.banks[0x3E][0] != 0x00

def generate_name(l, i):
    if i < len(l):
        name = l[i]
    else:
        name = f"player {i}"
    name = name[:16]
    assert(len(name) <= 16)
    return 'db "' + name + '"' + ', $ff' * (17 - len(name)) + '\n'


# Bank $3E is used for large chunks of custom code.
#   Mainly for new chest and dropped items handling.
def addBank3E(rom, seed, player_id, player_name_list):
    # No default text for getting the bow, so use an unused slot.
    rom.texts[0x89] = formatText("Found the {BOW}!")
    rom.texts[0xD9] = formatText("Found the {BOOMERANG}!")  # owl text slot reuse
    rom.texts[0xBE] = rom.texts[0x111]  # owl text slot reuse to get the master skull message in the first dialog group
    rom.texts[0xC8] = formatText("Found {BOWWOW}! Which monster put him in a chest? He is a good boi, and waits for you at the Swamp.")
    rom.texts[0xC9] = 0xC0A0  # Custom message slot
    rom.texts[0xCA] = formatText("Found {ARROWS_10}!")
    rom.texts[0xCB] = formatText("Found a {SINGLE_ARROW}... joy?")

    # Create a trampoline to bank 0x3E in bank 0x00.
    # There is very little room in bank 0, so we set this up as a single trampoline for multiple possible usages.
    # the A register is preserved and can directly be used as a jumptable in page 3E.
    # Trampoline at rst 8
    # the A register is preserved and can directly be used as a jumptable in page 3E.
    rom.patch(0, 0x0008, "0000000000000000000000000000", ASM("""
        ld   h, a
        ld   a, [$DBAF]
        push af
        ld   a, $3E
        call $080C ; switch bank
        ld   a, h
        jp $4000
    """), fill_nop=True)

    # Special trampoline to jump to the damage-entity code, we use this from bowwow to damage instead of eat.
    rom.patch(0x00, 0x0018, "000000000000000000000000000000", ASM("""
        ld   a, $03
        ld   [$2100], a
        call $71C0
        ld   a, [$DBAF]
        ld   [$2100], a
        ret
    """))

    def get_asm(name):
        return pkgutil.get_data(__name__, "bank3e.asm/" + name).decode().replace("\r", "")

    rom.patch(0x3E, 0x0000, 0x2F00, ASM("""
        call MainJumpTable
        pop af
        jp $080C ; switch bank and return to normal code.

MainJumpTable:
        rst  0 ; JUMP TABLE
        dw   MainLoop                             ; 0
        dw   RenderChestItem                      ; 1
        dw   GiveItemFromChest                    ; 2
        dw   ItemMessage                          ; 3
        dw   RenderDroppedKey                     ; 4
        dw   RenderHeartPiece                     ; 5
        dw   GiveItemFromChestMultiworld          ; 6
        dw   CheckIfLoadBowWow                    ; 7
        dw   BowwowEat                            ; 8
        dw   HandleOwlStatue                      ; 9
        dw   ItemMessageMultiworld                ; A
        dw   GiveItemAndMessageForRoom            ; B
        dw   RenderItemForRoom                    ; C
        dw   StartGameMarinMessage                ; D
        dw   GiveItemAndMessageForRoomMultiworld  ; E
        dw   RenderOwlStatueItem                  ; F
        dw   UpdateInventoryMenu                  ; 10
        dw   LocalOnlyItemAndMessage              ; 11
StartGameMarinMessage:
        ; Injection to reset our frame counter
        call $27D0 ; Enable SRAM
        ld   hl, $B000
        xor  a
        ldi  [hl], a ;subsecond counter
        ld   a, $08  ;(We set the counter to 8 seconds, as it takes 8 seconds before link wakes up and marin talks to him)
        ldi  [hl], a ;second counter
        xor  a
        ldi  [hl], a ;minute counter
        ldi  [hl], a ;hour counter

        ld   hl, $B010
        ld   a, $01  ;tarin's gift gets skipped for some reason, so inflate count by 1
        ldi  [hl], a ;check counter low
        xor  a
        ldi  [hl], a ;check counter high

        ; Show the normal message
        ld   a, $01
        jp $2385

TradeSequenceItemData:
    ; tile attributes
    db $0D, $0A, $0D, $0D, $0E, $0E, $0D, $0D, $0D, $0E, $09, $0A, $0A, $0D
    ; tile index
    db $1A, $B0, $B4, $B8, $BC, $C0, $C4, $C8, $CC, $D0, $D4, $D8, $DC, $E0

UpdateInventoryMenu:
        ld   a, [wTradeSequenceItem]
        ld   hl, wTradeSequenceItem2
        or   [hl]
        ret  z
        
        ld   hl, TradeSequenceItemData
        ld   a, [$C109]
        ld   e, a
        ld   d, $00
        add  hl, de

        ; Check if we need to increase the counter
        ldh  a, [$E7] ; frame counter
        and  $0F
        jr   nz, .noInc
        ld   a, e
        inc  a
        cp   14
        jr   nz, .noWrap
        xor  a
.noWrap:
        ld   [$C109], a
.noInc:

        ; Check if we have the item
        ld   b, e
        inc  b
        ld   a, $01

        ld   de, wTradeSequenceItem
.shiftLoop:
        dec  b
        jr   z, .shiftLoopDone
        sla  a
        jr   nz, .shiftLoop
        ; switching to second byte
        ld   de, wTradeSequenceItem2
        ld   a, $01
        jr   .shiftLoop
.shiftLoopDone:
        ld   b, a
        ld   a, [de]
        and  b
        ret  z ; skip this item

        ld   b, [hl]
        push hl

        ; Write the tile attribute data
        ld   a, $01
        ldh  [$4F], a

        ld   hl, $9C6E
        call WriteToVRAM
        inc  hl  
        call WriteToVRAM
        ld   de, $001F
        add  hl, de
        call WriteToVRAM
        inc  hl  
        call WriteToVRAM

        ; Write the tile data
        xor  a
        ldh  [$4F], a
        
        pop  hl
        ld   de, 14
        add  hl, de
        ld   b, [hl]
        
        ld   hl, $9C6E
        call WriteToVRAM
        inc  b
        inc  b
        inc  hl  
        call WriteToVRAM
        ld   de, $001F
        add  hl, de
        dec  b
        call WriteToVRAM
        inc  hl  
        inc  b
        inc  b
        call WriteToVRAM
        ret

WriteToVRAM:
        ldh  a, [$41]
        and  $02
        jr   nz, WriteToVRAM
        ld   [hl], b
        ret
LocalOnlyItemAndMessage:
        call GiveItemFromChest
        call ItemMessage
        ret
    """ + get_asm("multiworld.asm")
        + get_asm("link.asm")
        + get_asm("chest.asm")
        + get_asm("bowwow.asm")
        + get_asm("message.asm")
        + get_asm("itemnames.asm")
        + "".join(generate_name(["The Server"] + player_name_list, i ) for i in range(100)) # allocate
        + 'db "another world", $ff\n'
        + get_asm("owl.asm"), 0x4000), fill_nop=True)
    # 3E:3300-3616: Multiworld flags per room (for both chests and dropped keys)
    # 3E:3800-3B16: DroppedKey item types
    # 3E:3B16-3E2C: Owl statue or trade quest items
    
    # Put 20 rupees in all owls by default.
    rom.patch(0x3E, 0x3B16, "00" * 0x316, "1C" * 0x316)
   

    # Prevent the photo album from crashing due to serial interrupts
    rom.patch(0x28, 0x00D2, ASM("ld a, $09"), ASM("ld a, $01"))
