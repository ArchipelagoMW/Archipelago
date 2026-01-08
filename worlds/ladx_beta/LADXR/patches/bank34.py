import os
import binascii
import pkgutil

from ..assembler import ASM
from ..utils import formatText

ItemNameLookupTable = 0x0100
ItemNameLookupSize = 2
TotalRoomCount = 0x316

AnItemText = "an item"
ItemNameStringBufferStart = ItemNameLookupTable + \
    TotalRoomCount * ItemNameLookupSize


def addBank34(rom, item_list):
    rom.patch(0x34, 0x0000, ItemNameLookupTable, ASM("""
        ; Get the pointer in the lookup table, doubled as it's two bytes
        ld  hl, $2080
        push de
        call OffsetPointerByRoomNumber
        pop de
        add  hl, hl

        ldi  a, [hl] ; hl = *hl
        ld   h, [hl]
        ld   l, a

        ; If there's no data, bail
        ld a, l
        or h
        jp z, SwitchBackTo3E

        ld   de, wCustomMessage
        ; Copy in our item name
        call   MessageCopyString
    SwitchBackTo3E:
        ; Bail
        ld   a,  $3e   ; Set bank number
        jp   $080C ; switch bank

    ; this should be shared but I got link errors            
    OffsetPointerByRoomNumber:
        ldh  a, [$FFF6] ; map room
        ld   e, a
        ld   a, [$DBA5] ; is indoor
        ld   d, a
        ldh  a, [$FFF7]   ; mapId
        cp   $FF
        jr   nz, .notColorDungeon

        ld   d, $03
        jr   .notCavesA

    .notColorDungeon:
        cp   $1A
        jr   nc, .notCavesA
        cp   $06
        jr   c, .notCavesA
        inc  d
    .notCavesA:
        add  hl, de
        ret
    """ + pkgutil.get_data(__name__, "bank3e.asm/message.asm").decode().replace("\r", ""), 0x4000), fill_nop=True)

    nextItemLookup = ItemNameStringBufferStart
    nameLookup = {

    }

    def add_or_get_name(name):
        nonlocal nextItemLookup
        if name in nameLookup:
            return nameLookup[name]
        if len(name) + 1 + nextItemLookup >= 0x4000:
            return nameLookup[AnItemText]
        # Item names of exactly 255 characters will cause overwrites to occur in the text box
        # Custom text is only 95 bytes long, restrict to 4 lines (64)
        formatted = formatText("Got " + name, skip_names=True)[:-1][:59] # strip \xff before truncating
        # make room for 'for'/'from'
        last_len = len(formatted) % 16
        if 16 > last_len > 11: # push to new line
            for _ in range(last_len, 16):
                formatted += b' '
        formatted += b'\xff'

        rom.patch(0x34, nextItemLookup, None, binascii.hexlify(formatted))
        patch_len = len(formatted)
        nameLookup[name] = nextItemLookup + 0x4000
        nextItemLookup += patch_len
        return nameLookup[name]

    add_or_get_name(AnItemText)

    def swap16(x):
        assert x <= 0xFFFF
        return (x >> 8) | ((x & 0xFF) << 8)

    def to_hex_address(x):
        return f"{swap16(x):04x}"

    # Set defaults for every room
    for i in range(TotalRoomCount):
        rom.patch(0x34, ItemNameLookupTable + i *
                ItemNameLookupSize, None, to_hex_address(0))

    for item in item_list:
        if not item.custom_item_name:
            continue
        assert item.room < TotalRoomCount, item.room
        addr = add_or_get_name(item.custom_item_name)
        rom.patch(0x34, ItemNameLookupTable + item.room *
                  ItemNameLookupSize, None, to_hex_address(addr))
        if item.extra:
            rom.patch(0x34, ItemNameLookupTable + item.extra *
                  ItemNameLookupSize, None, to_hex_address(addr))