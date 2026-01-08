from ..assembler import ASM
from ..roomEditor import RoomEditor, ObjectHorizontal, ObjectVertical, Object
from .. import entityData


def addMultiworldShop(rom, this_player, player_count):
    # Make a copy of the shop into GrandpaUlrira house
    re = RoomEditor(rom, 0x2A9)
    re.objects = [
        ObjectHorizontal(1,1, 0x00, 8),
        ObjectHorizontal(1,2, 0x00, 8),
        ObjectHorizontal(1,3, 0xCD, 8),
        Object(2, 0, 0xC7),
        Object(7, 0, 0xC7),
        Object(7, 7, 0xFD),
    ] + re.getWarps()
    re.entities = [(0, 6, 0xD4)]
    for n in range(player_count):
        if n != this_player:
            re.entities.append((n + 1, 6, 0xD4))
    re.animation_id = 0x04
    re.floor_object = 0x0D
    re.store(rom)
    # Fix the tileset
    rom.banks[0x20][0x2EB3 + 0x2A9 - 0x100] = rom.banks[0x20][0x2EB3 + 0x2A1 - 0x100]

    re = RoomEditor(rom, 0x0B1)
    re.getWarps()[0].target_x = 128
    re.store(rom)

    # Load the shopkeeper sprites
    entityData.SPRITE_DATA[0xD4] = entityData.SPRITE_DATA[0x4D]
    rom.patch(0x03, 0x01CF, "00", "98") # Fix the hitbox of the ghost to be 16x16

    # Patch Ghost to work as a multiworld shop
    rom.patch(0x19, 0x1E18, 0x20B0, ASM("""
    ld   a, $01
    ld   [$C50A], a ; this stops link from using items

    ldh  a, [$FFEE] ; X
    cp   $08
    ; Jump to other code which is placed on the old owl code. As we do not have enough space here.
    jp   z, shopItemsHandler

;Draw shopkeeper
    ld   de, OwnerSpriteData
    call $3BC0 ; render sprite pair
    ldh  a, [$FFE7] ; frame counter
    swap a
    and  $01
    call $3B0C ; set sprite variant

    ldh  a, [$FFF0]
    and  a
    jr   nz, checkTalkingResult

    call $7CA2 ; prevent link from moving into the sprite
    call $7CF0 ; check if talking to NPC
    call c, talkHandler ; talk handling
    ret

checkTalkingResult:
    ld   a, [$C19F]
    and  a
    ret  nz ; still taking
    call $3B12 ; increase entity state
    ld   [hl], $00
    ld   a, [$C177] ; dialog selection
    and  a
    ret  nz
    jp TalkResultHandler

OwnerSpriteData:
    ;db   $60, $03, $62, $03, $62, $23, $60, $23 ; down
    db   $64, $03, $66, $03, $66, $23, $64, $23 ; up
    ;db   $68, $03, $6A, $03, $6C, $03, $6E, $03 ; left
    ;db   $6A, $23, $68, $23, $6E, $23, $6C, $23 ; right

shopItemsHandler:
; Render the shop items
    ld   h, $00
loop:
    ; First load links position to render the item at
    ldh  a, [$FF98] ; LinkX
    ldh  [$FFEE], a ; X
    ldh  a, [$FF99] ; LinkY
    sub  $0E
    ldh  [$FFEC], a ; Y
    ; Check if this is the item we have picked up
    ld   a, [$C509] ; picked up item in shop
    dec  a
    cp   h
    jr   z, .renderCarry

    ld   a, h
    swap a
    add  a, $20
    ldh  [$FFEE], a ; X
    ld   a, $30
    ldh  [$FFEC], a ; Y
.renderCarry:
    ld   a, h
    push hl
    ldh  [$FFF1], a ; variant
    cp   $03
    jr   nc, .singleSprite
    ld   de, ItemsDualSpriteData
    call $3BC0 ; render sprite pair
    jr   .renderDone
.singleSprite:
    ld   de, ItemsSingleSpriteData
    call $3C77 ; render sprite
.renderDone:

    pop  hl
.skipItem:
    inc  h
    ld   a, $07
    cp   h
    jr   nz, loop

;   check if we want to pickup or drop an item
    ldh  a, [$FFCC]
    and  $30 ; A or B button
    call nz, checkForPickup

;   check if we have an item
    ld   a, [$C509] ; carry item
    and  a
    ret  z

    ; Set that link has picked something up
    ld   a, $01
    ld   [$C15C], a
    call $0CAF ; reset spin attack...

    ; Check if we are trying to exit the shop and so drop our item.
    ldh  a, [$FF99]
    cp   $78
    ret  c
    xor  a
    ld   [$C509], a

    ret

checkForPickup:
    ldh  a, [$FF9E] ; direction
    cp   $02
    ret  nz
    ldh  a, [$FF99] ; LinkY
    cp   $48
    ret  nc

    ld   a, $13
    ldh  [$FFF2], a ; play SFX

    ld   a, [$C509] ; picked up shop item
    and  a
    jr   nz, .drop

    ldh  a, [$FF98] ; LinkX
    sub  $08
    swap a
    and  $07
    ld   [$C509], a ; picked up shop item
    ret
.drop:
    xor  a
    ld   [$C509], a
    ret

ItemsDualSpriteData:
    db   $60, $08, $60, $28 ; zol
    db   $68, $09 ; chicken (left)
ItemsSingleSpriteData: ; (first 3 entries are still dual sprites)
    db   $6A, $09 ; chicken (right)
    db   $14, $02, $14, $22 ; piece of power
;Real single sprite data starts here
    db   $00, $0F ; bomb
    db   $38, $0A ; rupees
    db   $20, $0C ; medicine
    db   $28, $0C ; heart

;------------------------------------trying to buy something starts here
talkHandler:
    ld   a, [$C509] ; carry item
    add  a, a
    ret  z ; check if we have something to buy
    sub  $02

    ld   hl, itemNames
    ld   e, a
    ld   d, b ; b=0
    add  hl, de
    ld   e, [hl]
    inc  hl
    ld   d, [hl]

    ld   hl, wCustomMessage
    call appendString
    dec  hl
    call padString
    ld   de, postMessage
    call appendString
    dec  hl
    ld   a, $fe
    ld   [hl], a
    ld   de, $FFEF
    add  hl, de
    ldh  a, [$FFEE]
    swap a
    and  $0F
    add  a, $30
    ld   [hl], a
    ld   a, $C9
    call $2385 ; open dialog
    call $3B12 ; increase entity state
    ret

appendString:
    ld   a, [de]
    inc  de
    and  a
    ret  z
    ldi  [hl], a
    jr   appendString

padString:
    ld   a, l
    and  $0F
    ret  z
    ld   a, $20
    ldi  [hl], a
    jr   padString

itemNames:
    dw itemZol
    dw itemChicken
    dw itemPieceOfPower
    dw itemBombs
    dw itemRupees
    dw itemMedicine
    dw itemHealth

postMessage:
    db  "For player X?       Yes  No  ", $00

itemZol:
    db  m"Slime storm|100 {RUPEES}", $00
itemChicken:
    db  m"Coccu party|50 {RUPEES}", $00
itemPieceOfPower:
    db  m"Piece of Power|50 {RUPEES}", $00
itemBombs:
    db  m"10 Bombs|50 {RUPEES}", $00
itemRupees:
    db  m"100 {RUPEES}|200 {RUPEES}", $00
itemMedicine:
    db  m"Medicine|100 {RUPEES}", $00
itemHealth:
    db  m"Health refill|10 {RUPEES}", $00

TalkResultHandler:
    ld  hl, ItemPriceTableBCD
    ld  a, [$C509]
    dec a
    add a, a
    ld  c, a ; b=0
    add hl, bc
    ldi a, [hl]
    ld  d, [hl]
    ld  e, a
    ld  a, [$DB5D]
    cp  d
    ret c
    jr  nz, .highEnough
    ld  a, [$DB5E]
    cp  e
    ret c
.highEnough:
    ; Got enough money, take it.
    ld  hl, ItemPriceTableDEC
    ld  a, [$C509]
    dec a
    ld  c, a ; b=0
    add hl, bc
    ld  a, [hl]
    ld  [$DB92], a ; set substract buffer
    
    ; Set the item to send
    ld  hl, $DDFE
    ld  a, [$C509] ; currently picked up item 
    ldi [hl], a
    ldh a, [$FFEE]   ; X position of NPC
    ldi [hl], a
    ld  hl, $DDF7
    set 2, [hl]

    ; No longer picked up item
    xor a
    ld  [$C509], a
    ret

ItemPriceTableBCD:
    dw $0100, $0050, $0050, $0050, $0200, $0100, $0010
ItemPriceTableDEC:
    db $64, $32, $32, $32, $C8, $64, $0A
    """, 0x5E18), fill_nop=True)
