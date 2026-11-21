RenderChestItem:
    ldh  a, [$F1] ; active sprite
    and  $80
    jr   nz, .renderLargeItem

    ld   de, ItemSpriteTable
    call $3C77 ; RenderActiveEntitySprite
    ret
.renderLargeItem:
    ld   de, LargeItemSpriteTable
    dec  d
    dec  d
    call $3BC0 ; RenderActiveEntitySpritePair

    ; If we are an instrument
    ldh  a, [$F1]
    cp   $8E
    ret  c
    cp   $96
    ret  nc

    ; But check if we are not state >3 before that, else the fade-out at the instrument room breaks.
    ldh  a, [$F0] ; hActiveEntityState
    cp   $03
    ret  nc

    ; Call the color cycling code
    xor  a
    ld   [$DC82], a
    ld   [$DC83], a
    ld   a, $3e
    call $0AD2
    ret

GiveItemFromChestMultiworld:
    call IncreaseCheckCounter
    ; Check our "item is for other player" flag
    ld   hl, $7300
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ld   hl, $0055
    cp   [hl]
    ret nz
    
GiveItemFromChest:
    ldh  a, [$F1] ; Load active sprite variant

    rst  0 ; JUMP TABLE
    dw ChestPowerBracelet; CHEST_POWER_BRACELET
    dw ChestShield       ; CHEST_SHIELD
    dw ChestBow          ; CHEST_BOW
    dw ChestWithItem     ; CHEST_HOOKSHOT
    dw ChestWithItem     ; CHEST_MAGIC_ROD
    dw Boots             ; CHEST_PEGASUS_BOOTS
    dw ChestWithItem     ; CHEST_OCARINA
    dw ChestWithItem     ; CHEST_FEATHER
    dw ChestWithItem     ; CHEST_SHOVEL
    dw ChestMagicPowder  ; CHEST_MAGIC_POWDER_BAG
    dw ChestBomb         ; CHEST_BOMB
    dw ChestSword        ; CHEST_SWORD
    dw Flippers          ; CHEST_FLIPPERS
    dw NoItem            ; CHEST_MAGNIFYING_LENS
    dw ChestWithItem    ; Boomerang (used to be unused)
    dw SlimeKey         ; ?? right side of your trade quest item
    dw Medicine         ; CHEST_MEDICINE
    dw TailKey          ; CHEST_TAIL_KEY
    dw AnglerKey        ; CHEST_ANGLER_KEY
    dw FaceKey          ; CHEST_FACE_KEY
    dw BirdKey          ; CHEST_BIRD_KEY
    dw GoldenLeaf       ; CHEST_GOLD_LEAF
    dw ChestWithCurrentDungeonItem ; CHEST_MAP
    dw ChestWithCurrentDungeonItem ; CHEST_COMPASS
    dw ChestWithCurrentDungeonItem ; CHEST_STONE_BEAK
    dw ChestWithCurrentDungeonItem ; CHEST_NIGHTMARE_KEY
    dw ChestWithCurrentDungeonItem ; CHEST_SMALL_KEY
    dw AddRupees50      ; CHEST_RUPEES_50
    dw AddRupees20      ; CHEST_RUPEES_20
    dw AddRupees100     ; CHEST_RUPEES_100
    dw AddRupees200     ; CHEST_RUPEES_200
    dw AddRupees500     ; CHEST_RUPEES_500
    dw AddSeashell      ; CHEST_SEASHELL
    dw NoItem           ; CHEST_MESSAGE
    dw NoItem           ; CHEST_GEL
    dw AddKey ; KEY1
    dw AddKey ; KEY2
    dw AddKey ; KEY3
    dw AddKey ; KEY4
    dw AddKey ; KEY5
    dw AddKey ; KEY6
    dw AddKey ; KEY7
    dw AddKey ; KEY8
    dw AddKey ; KEY9
    dw AddMap ; MAP1
    dw AddMap ; MAP2
    dw AddMap ; MAP3
    dw AddMap ; MAP4
    dw AddMap ; MAP5
    dw AddMap ; MAP6
    dw AddMap ; MAP7
    dw AddMap ; MAP8
    dw AddMap ; MAP9
    dw AddCompass ; COMPASS1
    dw AddCompass ; COMPASS2
    dw AddCompass ; COMPASS3
    dw AddCompass ; COMPASS4
    dw AddCompass ; COMPASS5
    dw AddCompass ; COMPASS6
    dw AddCompass ; COMPASS7
    dw AddCompass ; COMPASS8
    dw AddCompass ; COMPASS9
    dw AddStoneBeak ; STONE_BEAK1
    dw AddStoneBeak ; STONE_BEAK2
    dw AddStoneBeak ; STONE_BEAK3
    dw AddStoneBeak ; STONE_BEAK4
    dw AddStoneBeak ; STONE_BEAK5
    dw AddStoneBeak ; STONE_BEAK6
    dw AddStoneBeak ; STONE_BEAK7
    dw AddStoneBeak ; STONE_BEAK8
    dw AddStoneBeak ; STONE_BEAK9
    dw AddNightmareKey ; NIGHTMARE_KEY1
    dw AddNightmareKey ; NIGHTMARE_KEY2
    dw AddNightmareKey ; NIGHTMARE_KEY3
    dw AddNightmareKey ; NIGHTMARE_KEY4
    dw AddNightmareKey ; NIGHTMARE_KEY5
    dw AddNightmareKey ; NIGHTMARE_KEY6
    dw AddNightmareKey ; NIGHTMARE_KEY7
    dw AddNightmareKey ; NIGHTMARE_KEY8
    dw AddNightmareKey ; NIGHTMARE_KEY9
    dw AddToadstool ; Toadstool
    dw NoItem ; $51
    dw NoItem ; $52
    dw NoItem ; $53
    dw NoItem ; $54
    dw NoItem ; $55
    dw NoItem ; $56
    dw NoItem ; $57
    dw NoItem ; $58
    dw NoItem ; $59
    dw NoItem ; $5A
    dw NoItem ; $5B
    dw NoItem ; $5C
    dw NoItem ; $5D
    dw NoItem ; $5E
    dw NoItem ; $5F
    dw NoItem ; $60
    dw NoItem ; $61
    dw NoItem ; $62
    dw NoItem ; $63
    dw NoItem ; $64
    dw NoItem ; $65
    dw NoItem ; $66
    dw NoItem ; $67
    dw NoItem ; $68
    dw NoItem ; $69
    dw NoItem ; $6A
    dw NoItem ; $6B
    dw NoItem ; $6C
    dw NoItem ; $6D
    dw NoItem ; $6E
    dw NoItem ; $6F
    dw NoItem ; $70
    dw NoItem ; $71
    dw NoItem ; $72
    dw NoItem ; $73
    dw NoItem ; $74
    dw NoItem ; $75
    dw NoItem ; $76
    dw NoItem ; $77
    dw NoItem ; $78
    dw NoItem ; $79
    dw NoItem ; $7A
    dw NoItem ; $7B
    dw NoItem ; $7C
    dw NoItem ; $7D
    dw NoItem ; $7E
    dw NoItem ; $7F
    dw PieceOfHeart     ; Heart piece
    dw GiveBowwow
    dw Give10Arrows
    dw Give1Arrow
    dw UpgradeMaxPowder
    dw UpgradeMaxBombs
    dw UpgradeMaxArrows
    dw GiveRedTunic
    dw GiveBlueTunic
    dw GiveExtraHeart
    dw TakeHeart
    dw GiveSong1
    dw GiveSong2
    dw GiveSong3
    dw GiveInstrument
    dw GiveInstrument
    dw GiveInstrument
    dw GiveInstrument
    dw GiveInstrument
    dw GiveInstrument
    dw GiveInstrument
    dw GiveInstrument
    dw GiveRooster
    dw GiveTradeItem1
    dw GiveTradeItem2
    dw GiveTradeItem3
    dw GiveTradeItem4
    dw GiveTradeItem5
    dw GiveTradeItem6
    dw GiveTradeItem7
    dw GiveTradeItem8
    dw GiveTradeItem9
    dw GiveTradeItem10
    dw GiveTradeItem11
    dw GiveTradeItem12
    dw GiveTradeItem13
    dw GiveTradeItem14

NoItem:
    ret

ChestPowerBracelet:
    ld   hl, $DB43 ; power bracelet level
    jr   ChestIncreaseItemLevel

ChestShield:
    ld   hl, $DB44 ; shield level
    jr   ChestIncreaseItemLevel

ChestSword:
    ld   hl, $DB4E ; sword level
    jr   ChestIncreaseItemLevel

ChestIncreaseItemLevel:
    ld   a, [hl]
    cp   $02
    jr   z, DoNotIncreaseItemLevel
    inc  [hl]
DoNotIncreaseItemLevel:
    jp   ChestWithItem

ChestBomb:
    ld   a, [$DB4D] ; bomb count
    add  a, $10
    daa
    ld   hl, $DB77 ; max bombs
    cp   [hl]
    jr   c, .bombsNotFull
    ld   a, [hl]
.bombsNotFull:
    ld   [$DB4D], a
    jp   ChestWithItem

ChestBow:
    ld   a, [$DB45]
    cp   $20
    jp   nc, ChestWithItem
    ld   a, $20
    ld   [$DB45], a
    jp   ChestWithItem

ChestMagicPowder:
    ; Reset the toadstool state
    ld   a, $0B
    ldh  [$A5], a
    xor  a
    ld   [$DB4B], a ; has toadstool

    ld   a, [$DB4C] ; powder count
    add  a, $10
    daa
    ld   hl, $DB76 ; max powder
    cp   [hl]
    jr   c, .magicPowderNotFull
    ld   a, [hl]
.magicPowderNotFull:
    ld   [$DB4C], a
    jp   ChestWithItem

Boots:
    ; We use DB6D to store which tunics we have available
    ; ...and the boots
    ld  a, [wCollectedTunics]
    or  $04
    ld  [wCollectedTunics], a
    jp  ChestWithItem

Flippers:
    ld   a, $01
    ld   [wHasFlippers], a
    ret

Medicine:
    ld   a, $01
    ld   [wHasMedicine], a
    ret

TailKey:
    ld   a, $01
    ld   [$DB11], a
    ret

AnglerKey:
    ld   a, $01
    ld   [$DB12], a
    ret

FaceKey:
    ld   a, $01
    ld   [$DB13], a
    ret

BirdKey:
    ld   a, $01
    ld   [$DB14], a
    ret

SlimeKey:
    ld   a, $01
    ld   [$DB15], a
    ret

GoldenLeaf:
    ld   hl, wGoldenLeaves
    inc  [hl]
    ret

AddSeaShell:
    ld   a, [wSeashellsCount]
    inc  a
    daa
    ld   [wSeashellsCount], a
    ret

PieceOfHeart:
#IF HARD_MODE
    ld   a, $FF
    ld   [$DB93], a
#ENDIF

    ld   a, [$DB5C]
    inc  a
    cp   $04
    jr   z, .FullHeart
    ld   [$DB5C], a
    ret
.FullHeart:
    xor  a
    ld   [$DB5C], a
    jp   GiveExtraHeart

GiveBowwow:
    ld   a, $01
    ld   [$DB56], a
    ret

ChestInventoryTable:
    db   $03 ; CHEST_POWER_BRACELET
    db   $04 ; CHEST_SHIELD
    db   $05 ; CHEST_BOW
    db   $06 ; CHEST_HOOKSHOT
    db   $07 ; CHEST_MAGIC_ROD
    db   $08 ; CHEST_PEGASUS_BOOTS
    db   $09 ; CHEST_OCARINA
    db   $0A ; CHEST_FEATHER
    db   $0B ; CHEST_SHOVEL
    db   $0C ; CHEST_MAGIC_POWDER_BAG
    db   $02 ; CHEST_BOMB
    db   $01 ; CHEST_SWORD
    db   $00 ; - (flippers slot)
    db   $00 ; - (magnifier lens slot)
    db   $0D ; Boomerang

ChestWithItem:
    ldh  a, [$F1] ; Load active sprite variant
    ld   d, $00
    ld   e, a
    ld   hl, ChestInventoryTable
    add  hl, de
    ld   d, [hl]
    call $3E6B ; Give Inventory
    ret

ChestWithCurrentDungeonItem:
    sub  $16 ; a -= CHEST_MAP
    ld   e, a
    ld   d, $00
    ld   hl, $DBCC ; hasDungeonMap
    add  hl, de
    inc  [hl]
    call $2802  ; Sync current dungeon items with dungeon specific table
    ret

AddToadstool:
    ld   d, $0E
    call $3E6B ; Give Inventory
    ret

AddKey:
    sub $23 ; Make 'A' target dungeon index
    ld   de, $0004
    jr   AddDungeonItem

AddMap:
    sub $2C ; Make 'A' target dungeon index
    ld   de, $0000
    jr   AddDungeonItem

AddCompass:
    sub $35 ; Make 'A' target dungeon index
    ld   de, $0001
    jr   AddDungeonItem

AddStoneBeak:
    sub $3E ; Make 'A' target dungeon index
    ld   de, $0002
    jr   AddDungeonItem

AddNightmareKey:
    sub $47 ; Make 'A' target dungeon index
    ld   de, $0003
    jr   AddDungeonItem

AddDungeonItem:
    cp   $08
    jr   z, .colorDungeon
    ; hl = dungeonitems + type_type + dungeon * 8
    ld   hl, $DB16
    add  hl, de
    push de
    ld   e, a
    add  hl, de
    add  hl, de
    add  hl, de
    add  hl, de
    add  hl, de
    pop  de
    inc  [hl]
    ; Check if we are in this specific dungeon, and then increase the copied counters as well.
    ld   hl, $FFF7   ; is current map == target map
    cp   [hl]
    ret  nz
    ld   a, [$DBA5] ; is indoor
    and  a
    ret  z

    ld   hl, $DBCC
    add  hl, de
    inc  [hl]
    ret
.colorDungeon:
    ; Special case for the color dungeon, which is in a different location in memory.
    ld   hl, $DDDA
    add  hl, de
    inc  [hl]
    ldh  a, [$F7]   ; is current map == color dungeon
    cp   $ff
    ret  nz
    ld   hl, $DBCC
    add  hl, de
    inc  [hl]
    ret

AddRupees20:
    ld   hl, $0014
    jr   AddRupees

AddRupees50:
    ld   hl, $0032
    jr   AddRupees

AddRupees100:
    ld   hl, $0064
    jr   AddRupees

AddRupees200:
    ld   hl, $00C8
    jr   AddRupees

AddRupees500:
    ld   hl, $01F4
    jr   AddRupees

AddRupees:
    ld  a, [$DB8F]
    ld  d, a
    ld  a, [$DB90]
    ld  e, a
    add hl, de
    ld  a, h
    ld  [$DB8F], a
    ld  a, l
    ld  [$DB90], a
    ld   a, $18
    ld   [$C3CE], a
    ret

Give1Arrow:
    ld   a, [$DB45]
    inc  a
    jp   FinishGivingArrows

Give10Arrows:
    ld   a, [$DB45]
    add  a, $0A
FinishGivingArrows:
    daa
    ld   [$DB45], a
    ld   hl, $DB78
    cp   [hl]
    ret  c
    ld   a, [hl]
    ld   [$DB45], a
    ret

UpgradeMaxPowder:
    ld   a, $40
    ld   [$DB76], a
    ; If we have no powder, we should not increase the current amount, as that would prevent
    ; The toadstool from showing up.
    ld   a, [$DB4C]
    and  a
    ret  z
    ld   a, $40
    ld   [$DB4C], a
    ret

UpgradeMaxBombs:
    ld   a, $60
    ld   [$DB77], a
    ld   [$DB4D], a
    ret

UpgradeMaxArrows:
    ld   a, $60
    ld   [$DB78], a
    ld   [$DB45], a
    ret

GiveRedTunic:
    ld  a, $01
    ld  [$DC0F], a
    ; We use DB6D to store which tunics we have available.
    ld  a, [wCollectedTunics]
    or  $01
    ld  [wCollectedTunics], a
    ret

GiveBlueTunic:
    ld  a, $02
    ld  [$DC0F], a
    ; We use DB6D to store which tunics we have available.
    ld  a, [wCollectedTunics]
    or  $02
    ld  [wCollectedTunics], a
    ret

GiveExtraHeart:
    ; Regen all health
    ld   hl, $DB93
    ld   [hl], $FF
    ; Increase max health if health is lower then 14 hearts
    ld   hl, $DB5B
    ld   a, $0E
    cp   [hl]
    ret  z
    inc  [hl]
    ret

TakeHeart:
    ; First, reduce the max HP
    ld   hl, $DB5B
    ld   a, [hl]
    cp   $01
    ret  z
    dec  a
    ld   [$DB5B], a

    ; Next, check if we need to reduce our actual HP to keep it below the maximum.
    rlca
    rlca
    rlca
    sub  $01
    ld   hl, $DB5A
    cp   [hl]
    jr   nc, .noNeedToReduceHp
    ld   [hl], a
.noNeedToReduceHp:
    ; Finally, give all health back.
    ld   hl, $DB93
    ld   [hl], $FF
    ret

GiveSong1:
    ld   hl, $DB49
    set  2, [hl]
    ld   a, $00
    ld   [$DB4A], a
    ret

GiveSong2:
    ld   hl, $DB49
    set  1, [hl]
    ld   a, $01
    ld   [$DB4A], a
    ret

GiveSong3:
    ld   hl, $DB49
    set  0, [hl]
    ld   a, $02
    ld   [$DB4A], a
    ret

GiveInstrument:
    ldh  a, [$F1] ; Load active sprite variant
    sub  $8E
    ld   d, $00
    ld   e, a
    ld   hl, $db65 ; has instrument table
    add  hl, de
    set  1, [hl]
    ret

GiveRooster:
    ld   d, $0F
    call $3E6B ; Give Inventory (rooster item)

    ;ld   a, $01
    ;ld   [$DB7B], a ; has rooster
    ldh  a, [$F9] ; do not spawn rooster in sidescroller
    and  a
    ret  z

    ld   a, $D5 ; ENTITY_ROOSTER
    call $3B86 ; SpawnNewEntity_trampoline
    ldh  a, [$98] ; LinkX
    ld   hl, $C200 ; wEntitiesPosXTable
    add  hl, de
    ld   [hl], a
    ldh  a, [$99] ; LinkY
    ld   hl, $C210 ; wEntitiesPosYTable
    add  hl, de
    ld   [hl], a

    ret

GiveTradeItem1:
    ld   hl, wTradeSequenceItem
    set  0, [hl]
    ret
GiveTradeItem2:
    ld   hl, wTradeSequenceItem
    set  1, [hl]
    ret
GiveTradeItem3:
    ld   hl, wTradeSequenceItem
    set  2, [hl]
    ret
GiveTradeItem4:
    ld   hl, wTradeSequenceItem
    set  3, [hl]
    ret
GiveTradeItem5:
    ld   hl, wTradeSequenceItem
    set  4, [hl]
    ret
GiveTradeItem6:
    ld   hl, wTradeSequenceItem
    set  5, [hl]
    ret
GiveTradeItem7:
    ld   hl, wTradeSequenceItem
    set  6, [hl]
    ret
GiveTradeItem8:
    ld   hl, wTradeSequenceItem
    set  7, [hl]
    ret
GiveTradeItem9:
    ld   hl, wTradeSequenceItem2
    set  0, [hl]
    ret
GiveTradeItem10:
    ld   hl, wTradeSequenceItem2
    set  1, [hl]
    ret
GiveTradeItem11:
    ld   hl, wTradeSequenceItem2
    set  2, [hl]
    ret
GiveTradeItem12:
    ld   hl, wTradeSequenceItem2
    set  3, [hl]
    ret
GiveTradeItem13:
    ld   hl, wTradeSequenceItem2
    set  4, [hl]
    ret
GiveTradeItem14:
    ld   hl, wTradeSequenceItem2
    set  5, [hl]
    ret

ItemMessageMultiworld:
    ; Check our "item is for other player" flag
    ld   hl, $7300
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ld   hl, $0055
    cp   [hl]
    jr   nz, ItemMessageForOtherPlayer

ItemMessage:
    ; Fill the custom message slot with this item message.
    call BuildItemMessage
    ldh  a, [$F1]
    ld   d, $00
    ld   e, a
    ld   hl, ItemMessageTable
    add  hl, de
    ld   a, [hl]
    cp   $90
    jr   z, .powerBracelet
    cp   $3D
    jr   z, .shield
    jp   $2385 ; Opendialog in $000-$0FF range

.powerBracelet:
    ; Check the power bracelet level, and give a different message when we get the lv2 bracelet
    ld   hl, $DB43 ; power bracelet level
    bit  1, [hl]
    jp   z, $2385 ; Opendialog in $000-$0FF range
    ld   a, $EE
    jp   $2385 ; Opendialog in $000-$0FF range

.shield:
    ; Check the shield level, and give a different message when we get the lv2 shield
    ld   hl, $DB44 ; shield level
    bit  1, [hl]
    jp   z, $2385 ; Opendialog in $000-$0FF range
    ld   a, $ED
    jp   $2385 ; Opendialog in $000-$0FF range

ItemMessageForOtherPlayer:
    push bc
    push hl
    push af
    call BuildRemoteItemMessage
    ld hl, SpaceFor
    call MessageCopyString
    pop af
    call MessageAddPlayerName
    pop hl
    pop bc
    ;dec  de
    ld   a, $C9
    jp   $2385 ; Opendialog in $000-$0FF range

ItemSpriteTable:
    db $82, $15        ; CHEST_POWER_BRACELET
    db $86, $15        ; CHEST_SHIELD
    db $88, $14        ; CHEST_BOW
    db $8A, $14        ; CHEST_HOOKSHOT
    db $8C, $14        ; CHEST_MAGIC_ROD
    db $98, $16        ; CHEST_PEGASUS_BOOTS
    db $10, $1F        ; CHEST_OCARINA
    db $12, $1D        ; CHEST_FEATHER
    db $96, $17        ; CHEST_SHOVEL
    db $0E, $1C        ; CHEST_MAGIC_POWDER_BAG
    db $80, $15        ; CHEST_BOMB
    db $84, $15        ; CHEST_SWORD
    db $94, $15        ; CHEST_FLIPPERS
    db $9A, $10        ; CHEST_MAGNIFYING_LENS
    db $24, $1C        ; Boomerang
    db $4E, $1C        ; Slime key
    db $A0, $14        ; CHEST_MEDICINE
    db $30, $1C        ; CHEST_TAIL_KEY
    db $32, $1C        ; CHEST_ANGLER_KEY
    db $34, $1C        ; CHEST_FACE_KEY
    db $36, $1C        ; CHEST_BIRD_KEY
    db $3A, $1C        ; CHEST_GOLD_LEAF
    db $40, $1C        ; CHEST_MAP
    db $42, $1D        ; CHEST_COMPASS
    db $44, $1C        ; CHEST_STONE_BEAK
    db $46, $1C        ; CHEST_NIGHTMARE_KEY
    db $4A, $1F        ; CHEST_SMALL_KEY
    db $A6, $15        ; CHEST_RUPEES_50 (normal blue)
    db $38, $19        ; CHEST_RUPEES_20 (red)
    db $38, $18        ; CHEST_RUPEES_100 (green)
    db $38, $1A        ; CHEST_RUPEES_200 (yellow)
    db $38, $1A        ; CHEST_RUPEES_500 (yellow)
    db $9E, $14        ; CHEST_SEASHELL
    db $8A, $14        ; CHEST_MESSAGE
    db $A0, $14        ; CHEST_GEL
    db $4A, $1D        ; KEY1
    db $4A, $1D        ; KEY2
    db $4A, $1D        ; KEY3
    db $4A, $1D        ; KEY4
    db $4A, $1D        ; KEY5
    db $4A, $1D        ; KEY6
    db $4A, $1D        ; KEY7
    db $4A, $1D        ; KEY8
    db $4A, $1D        ; KEY9
    db $40, $1C        ; MAP1
    db $40, $1C        ; MAP2
    db $40, $1C        ; MAP3
    db $40, $1C        ; MAP4
    db $40, $1C        ; MAP5
    db $40, $1C        ; MAP6
    db $40, $1C        ; MAP7
    db $40, $1C        ; MAP8
    db $40, $1C        ; MAP9
    db $42, $1D        ; COMPASS1
    db $42, $1D        ; COMPASS2
    db $42, $1D        ; COMPASS3
    db $42, $1D        ; COMPASS4
    db $42, $1D        ; COMPASS5
    db $42, $1D        ; COMPASS6
    db $42, $1D        ; COMPASS7
    db $42, $1D        ; COMPASS8
    db $42, $1D        ; COMPASS9
    db $44, $1C        ; STONE_BEAK1
    db $44, $1C        ; STONE_BEAK2
    db $44, $1C        ; STONE_BEAK3
    db $44, $1C        ; STONE_BEAK4
    db $44, $1C        ; STONE_BEAK5
    db $44, $1C        ; STONE_BEAK6
    db $44, $1C        ; STONE_BEAK7
    db $44, $1C        ; STONE_BEAK8
    db $44, $1C        ; STONE_BEAK9
    db $46, $1C        ; NIGHTMARE_KEY1
    db $46, $1C        ; NIGHTMARE_KEY2
    db $46, $1C        ; NIGHTMARE_KEY3
    db $46, $1C        ; NIGHTMARE_KEY4
    db $46, $1C        ; NIGHTMARE_KEY5
    db $46, $1C        ; NIGHTMARE_KEY6
    db $46, $1C        ; NIGHTMARE_KEY7
    db $46, $1C        ; NIGHTMARE_KEY8
    db $46, $1C        ; NIGHTMARE_KEY9
    db $4C, $1C        ; Toadstool
    db $AE, $14        ; Guardian Acorn

LargeItemSpriteTable:
    db $AC, $02, $AC, $22 ; heart piece
    db $54, $0A, $56, $0A ; bowwow
    db $2A, $41, $2A, $61 ; 10 arrows
    db $2A, $41, $2A, $61 ; single arrow
    db $0E, $1C, $22, $0C ; powder upgrade
    db $00, $0D, $22, $0C ; bomb upgrade
    db $08, $1C, $22, $0C ; arrow upgrade
    db $48, $0A, $48, $2A ; red tunic
    db $48, $0B, $48, $2B ; blue tunic
    db $2A, $0C, $2A, $2C ; heart container
    db $2A, $0F, $2A, $2F ; bad heart container
    db $70, $09, $70, $29 ; song 1
    db $72, $0B, $72, $2B ; song 2
    db $74, $08, $74, $28 ; song 3
    db $80, $0E, $82, $0E ; Instrument1
    db $84, $0E, $86, $0E ; Instrument2
    db $88, $0E, $8A, $0E ; Instrument3
    db $8C, $0E, $8E, $0E ; Instrument4
    db $90, $0E, $92, $0E ; Instrument5
    db $94, $0E, $96, $0E ; Instrument6
    db $98, $0E, $9A, $0E ; Instrument7
    db $9C, $0E, $9E, $0E ; Instrument8
    db $A6, $2B, $A4, $2B ; Rooster
    db $1A, $0E, $1C, $0E ; TradeItem1
    db $B0, $0C, $B2, $0C ; TradeItem2
    db $B4, $0C, $B6, $0C ; TradeItem3
    db $B8, $0C, $BA, $0C ; TradeItem4
    db $BC, $0C, $BE, $0C ; TradeItem5
    db $C0, $0C, $C2, $0C ; TradeItem6
    db $C4, $0C, $C6, $0C ; TradeItem7
    db $C8, $0C, $CA, $0C ; TradeItem8
    db $CC, $0C, $CE, $0C ; TradeItem9
    db $D0, $0C, $D2, $0C ; TradeItem10
    db $D4, $0D, $D6, $0D ; TradeItem11
    db $D8, $0D, $DA, $0D ; TradeItem12
    db $DC, $0D, $DE, $0D ; TradeItem13
    db $E0, $0D, $E2, $0D ; TradeItem14
    db $14, $42, $14, $62 ; Piece Of Power

ItemMessageTable:
    db $90, $3D, $89, $93, $94, $95, $96, $97, $98, $99, $9A, $9B, $9C, $9D, $D9, $A2
    db $A0, $A1, $A3, $A4, $A5, $E8, $A6, $A7, $A8, $A9, $AA, $AC, $AB, $AD, $AE, $C9
    db $EF, $BE, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9
    db $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9
    ; $40
    db $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9
    db $0F, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
    db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
    db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
    ; $80
    db $4F, $C8, $CA, $CB, $E2, $E3, $E4, $CC, $CD, $2A, $2B, $C9, $C9, $C9, $C9, $C9
    db $C9, $C9, $C9, $C9, $C9, $C9, $B8, $44, $C9, $C9, $C9, $C9, $C9, $C9, $C9, $C9
    db $C9, $C9, $C9, $C9, $9D, $C9

RenderDroppedKey:
    ;TODO: See EntityInitKeyDropPoint for a few special cases to unload.

RenderHeartPiece:
    ; Check if our chest type is already loaded
    ld   hl, $C2C0
    add  hl, bc
    ld   a, [hl]
    and  a
    jr   nz, .droppedKeyTypeLoaded
    inc  [hl]

    ;Load the chest type from the chest table.
    ld   hl, $7800
    call OffsetPointerByRoomNumber

    ld   a, [hl]
    ldh  [$F1], a ; set currentEntitySpriteVariant
    call $3B0C ; SetEntitySpriteVariant

    and  $80
    ld   hl, $C340
    add  hl, bc
    ld   a, [hl]
    jr   z, .singleSprite
    ; We potentially need to fix the physics flags table to allocate 2 sprites for us
    and  $F8
    or   $02
    ld   [hl], a
    jr .droppedKeyTypeLoaded
.singleSprite:
    and  $F8
    or   $01
    ld   [hl], a
.droppedKeyTypeLoaded:
    jp RenderChestItem


OffsetPointerByRoomNumber:
    ldh  a, [$F6] ; map room
    ld   e, a
    ld   a, [$DBA5] ; is indoor
    ld   d, a
    ldh  a, [$F7]   ; mapId
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

GiveItemAndMessageForRoom:
    ;Load the chest type from the chest table.
    ld   hl, $7800
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ldh  [$F1], a
    call GiveItemFromChest
    jp ItemMessage

GiveItemAndMessageForRoomMultiworld:
    ;Load the chest type from the chest table.
    ld   hl, $7800
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ldh  [$F1], a
    call GiveItemFromChestMultiworld
    jp ItemMessageMultiworld

RenderItemForRoom:
    ;Load the chest type from the chest table.
    ld   hl, $7800
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ldh  [$F1], a
    jp   RenderChestItem

; Increase the amount of checks we completed, unless we are on the multichest room.
IncreaseCheckCounter:
    ldh  a, [$F6] ; map room
    cp   $F2
    jr   nz, .noMultiChest
    ld   a, [$DBA5] ; is indoor
    and  a
    jr   z, .noMultiChest
    ldh  a, [$F7]   ; mapId
    cp   $0A
    ret  z

.noMultiChest:
    call $27D0 ; Enable SRAM
    ld   hl, $B010
.loop:
    ld   a, [hl]
    and  a ; clear carry flag
    inc  a
    daa
    ldi  [hl], a
    ret  nc
    jr   .loop
