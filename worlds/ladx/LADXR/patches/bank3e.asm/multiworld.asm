; Handle the multiworld link

MainLoop:
    ; Check if the gameplay is world
    ld   a, [$DB95]
    cp   $0B
    ret  nz
    ; Check if the world subtype is the normal one
    ld   a, [$DB96]
    cp   $07
    ret  nz
    ; Check if we are moving between rooms
    ld   a, [$C124]
    and  a
    ret  nz
    ; Check if link is in a normal walking/swimming state
    ld   a, [$C11C]
    cp   $02
    ret  nc
    ; Check if a dialog is open
    ld   a, [$C19F]
    and  a
    ret  nz
    ; Check if interaction is blocked
    ldh  a, [$A1]
    and  a
    ret  nz

    ld   a, [wLinkSpawnDelay]
    and  a
    jr   z, .allowSpawn
    dec  a
    ld   [wLinkSpawnDelay], a
    jr   .noSpawn

.allowSpawn:
    ld   a, [wZolSpawnCount]
    and  a
    call nz, LinkSpawnSlime
    ld   a, [wCuccoSpawnCount]
    and  a
    call nz, LinkSpawnCucco
    ld   a, [wDropBombSpawnCount]
    and  a
    call nz, LinkSpawnBomb

    ; deathlink
    ld   hl, wMWCommand
    bit  3, [hl]
    jr   z, .noSpawn
    ld   a, [wMWDeathLinkRecv]
    jr   nz, .noSpawn ; if deathlink recv flag is still up, dont do it
    ld   a, [wHasMedicine]
    ; set health and health loss to a
    ; instant kill if no medicine
    ; kill with damage if medicine (to trigger medicine)
    ld   [$DB5A], a ; wHealth
    ld   [$DB94], a ; wSubtractHealthBuffer
    ; set health gain to zero
    xor  a
    ld   [$DB93], a ; wAddHealthBuffer
    ; flag deathlink as received
    ld   a, $01
    ld   [wMWDeathLinkRecv], a

.noSpawn:
    ; Have a location to collect?
    ld   hl, wMWCommand
    bit  2, [hl]
    jr   z, .noCollect
    ; get current location value onto b
    ld   a, [wMWMultipurposeC] ; collect location hi
    ld   h, a
    ld   a, [wMWMultipurposeD] ; collect location lo
    ld   l, a
    ld   a, [hl]
    ld   b, a
    ld   a, [wMWMultipurposeE] ; location mask
    or   b ; apply mask
    cp   b ; was location already set?
    jr   z, .clearAndRet ; if so, do nothing else
    ld   [hl], a

.noCollect:
    ; Have an item to give?
    ld   hl, wMWCommand
    bit  0, [hl]
    jr   z, .clearAndRet
    ld   hl, wMWCommand
    bit  1, [hl] ; do recvindex check only if bit set
    jr   z, .skipRecvIndexCheck
    ld   a, [wMWRecvIndexHi]
    ld   b, a
    ld   a, [wMWMultipurposeC]
    cp   b
    jr   nz, .clearAndRet ; failed check on hi
    ld   a, [wMWRecvIndexLo]
    ld   b, a
    ld   a, [wMWMultipurposeD]
    cp   b
    jr   nz, .clearAndRet ; failed check on lo
    ; increment recvindex
    ld   a, [wMWRecvIndexLo]
    inc  a
    ld   [wMWRecvIndexLo], a
    jr   nz, .skipRecvIndexCheck ; no overflow, done
    ld   a, [wMWRecvIndexHi]
    inc  a
    ld   [wMWRecvIndexHi], a

.skipRecvIndexCheck:
    ; Give an item to the player
    ld   a, [wMWItemCode]
    ; if zol:
    cp   $22 ; zol item
    jr   z, LinkGiveSlime
    ; if special item
    cp   $F0
    jr   nc, HandleSpecialItem
    ; tmpChestItem = a
    ldh  [$F1], a
    ; Give the item
    call GiveItemFromChest
    ; Paste the item text
    call BuildItemMessage
    ; Paste " from "
    ld hl, SpaceFrom
    call MessageCopyString
    ; Paste the player name
    ld  a, [wMWItemSenderLo]
    call MessageAddPlayerName
    xor  a
    ld   hl, wMWCommand
    ld   [hl], a
    ld   a, $C9
    ; OpenDialog()
    jp   $2385 ; Opendialog in $000-$0FF range

.clearAndRet:
    xor  a
    ld   hl, wMWCommand
    ld   [hl], a
    ret

LinkGiveSlime:
    ld   a, $05
    ld   [wZolSpawnCount], a
    ld   hl, wMWCommand
    res  0, [hl]
    ret

HandleSpecialItem:
    ld   hl, wMWCommand
    res  0, [hl]

    and  $0F
    rst  0
    dw SpecialSlimeStorm
    dw SpecialCuccoParty
    dw SpecialPieceOfPower
    dw SpecialHealth
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
.ret:
    ret

SpecialSlimeStorm:
    ld   a, $20
    ld   [wZolSpawnCount], a
    ret
SpecialCuccoParty:
    ld   a, $20
    ld   [wCuccoSpawnCount], a
    ret
SpecialPieceOfPower:
    ; Give the piece of power and the music
    ld   a, $01
    ld   [$D47C], a
    ld   a, $27
    ld   [$D368], a
    ld   a, $49
    ldh  [$BD], a
    ldh  [$BF], a
    ret
SpecialHealth:
    ; Regen all health
    ld   hl, $DB93
    ld   [hl], $FF
    ret

LinkSpawnSlime:
    ld   a, $1B
    ld   e, $08
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place somewhere random
    call placeRandom

    ld   hl, $C310
    add  hl, de
    ld   [hl], $7F

    ld   hl, wZolSpawnCount
    dec  [hl]

    call $280D
    and  $03
    ld   [wLinkSpawnDelay], a
    ret

LinkSpawnCucco:
    ld   a, $6C
    ld   e, $04
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place where link is at.
    ld   hl, $C200
    add  hl, de
    ldh  a, [$98]
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    ldh  a, [$99]
    ld   [hl], a

    ; Set the "hits till cucco killer attack" much lower
    ld   hl, $C2B0
    add  hl, de
    ld   a, $21
    ld   [hl], a

    ld   hl, wCuccoSpawnCount
    dec  [hl]

    call $280D
    and  $07
    ld   [wLinkSpawnDelay], a
    ret

LinkSpawnBomb:
    ld   a, $02
    ld   e, $08
    call $3B98 ; SpawnNewEntity in range
    ret  c

    call placeRandom

    ld   hl, $C310 ; z pos
    add  hl, de
    ld   [hl], $4F

    ld   hl, $C430 ; wEntitiesOptions1Table
    add  hl, de
    res  0, [hl]
    ld   hl, $C2E0 ; wEntitiesTransitionCountdownTable
    add  hl, de
    ld   [hl], $80
    ld   hl, $C440 ; wEntitiesPrivateState4Table
    add  hl, de
    ld   [hl], $01

    ld   hl, wDropBombSpawnCount
    dec  [hl]

    call $280D
    and  $1F
    ld   [wLinkSpawnDelay], a
    ret

placeRandom:
    ; Place somewhere random
    ld   hl, $C200
    add  hl, de
    call $280D ; random number
    and  $7F
    add  a, $08
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    call $280D ; random number
    and  $3F
    add  a, $20
    ld   [hl], a
    ret

Data_004_7AE5: ; @TODO Palette data
    db   $33, $62, $1A, $01, $FF, $0F, $FF, $7F

loop_7B32:
    ld   a, [de]                                  ; $7B32: $1A
    ; ld   [hl+], a                                 ; $7B33: $22
    db $22
    inc  de                                       ; $7B34: $13
    ld   a, l                                     ; $7B35: $7D
    and  $07                                      ; $7B36: $E6 $07
    jr   nz, loop_7B32                           ; $7B38: $20 $F8

    ld   a, $02                                   ; $7B3A: $3E $02
    ld   [$DDD1], a                              ; $7B3C: $EA $D1 $DD

    ret
