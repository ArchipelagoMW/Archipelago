; Handle the multiworld link

MainLoop:
#IF HARDWARE_LINK
    call handleSerialLink
#ENDIF
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
.noSpawn:

    ; Have an item to give?
    ld   hl, wLinkStatusBits
    bit  0, [hl]
    ret  z

    ; Give an item to the player
    ld   a, [wLinkGiveItem]
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
    ld  a, [wLinkGiveItemFrom]
    call MessageAddPlayerName
    ld   a, $C9
    ; hl = $wLinkStatusBits
    ld   hl, wLinkStatusBits
    ; clear the 0 bit of *hl
    res  0, [hl]
    ; OpenDialog()
    jp   $2385 ; Opendialog in $000-$0FF range

LinkGiveSlime:
    ld   a, $05
    ld   [wZolSpawnCount], a
    ld   hl, wLinkStatusBits
    res  0, [hl]
    ret

HandleSpecialItem:
    ld   hl, wLinkStatusBits
    res  0, [hl]

    and  $0F
    rst  0
    dw SpecialSlimeStorm
    dw SpecialCuccoParty
    dw SpecialPieceOfPower
    dw SpecialHealth
    dw SpecialRandomTeleport
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

SpecialRandomTeleport:
    xor  a
    ; Warp data
    ld   [$D401], a
    ld   [$D402], a
    call $280D ; random number
    ld   [$D403], a
    ld   hl, RandomTeleportPositions
    ld   d, $00
    ld   e, a
    add  hl, de
    ld   e, [hl]
    ld   a, e
    and  $0F
    swap a
    add  a, $08
    ld   [$D404], a
    ld   a, e
    and  $F0
    add  a, $10
    ld   [$D405], a

    ldh  a, [$98]
    swap a
    and  $0F
    ld   e, a
    ldh  a, [$99]
    sub  $08
    and  $F0
    or   e
    ld   [$D416], a ; wWarp0PositionTileIndex

    call $0C7D
    ld   a, $07
    ld   [$DB96], a ; wGameplaySubtype

    ret

Data_004_7AE5: ; @TODO Palette data
    db   $33, $62, $1A, $01, $FF, $0F, $FF, $7F


Deathlink:
    ; Spawn the entity
    ld   a, $CA               ; $7AF3: $3E $CA
    call $3B86                ; $7AF5: $CD $86 $3B  ;SpawnEntityTrampoline
    ld   a, $26               ; $7AF8: $3E $26      ;
    ldh  [$F4], a             ; $7AFA: $E0 $F4      ; set noise
    ; Set posX = linkX
    ldh  a, [$98] ; LinkX
    ld   hl, $C200 ; wEntitiesPosXTable
    add  hl, de
    ld   [hl], a
    ; set posY = linkY - 54
    ldh  a, [$99] ; LinkY
    sub  a, 54
    ld   hl, $C210 ; wEntitiesPosYTable
    add  hl, de
    ld   [hl], a
    ; wEntitiesPrivateState3Table
    ld   hl, $C2D0          ; $7B0A: $21 $D0 $C2
    add  hl, de                                   ; $7B0D: $19
    ld   [hl], $01                                ; $7B0E: $36 $01
    ; wEntitiesTransitionCountdownTable    
    ld   hl, $C2E0    ; $7B10: $21 $E0 $C2
    add  hl, de                                   ; $7B13: $19
    ld   [hl], $C0                                ; $7B14: $36 $C0
    ; GetEntityTransitionCountdown             
    call $0C05             ; $7B16: $CD $05 $0C
    ld   [hl], $C0                                ; $7B19: $36 $C0
    ; IncrementEntityState
    call $3B12                ; $7B1B: $CD $12 $3B

    ; Remove medicine
    xor  a                                        ; $7B1E: $AF
    ld   [$DB0D], a           ; $7B1F: $EA $0D $DB ; ld   [wHasMedicine], a
    ; Reduce health by a lot
    ld   a, $FF                                   ; $7B22: $3E $FF
    ld   [$DB94], a           ; $7B24: $EA $94 $DB ; ld   [wSubtractHealthBuffer], a

    ld   hl, $DC88                             ; $7B2C: $21 $88 $DC
    ; Set palette
    ld   de, Data_004_7AE5                        ; $7B2F: $11 $E5 $7A
    
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

; probalby wants
;     ld   a, $02                                   ; $7B40: $3E $02
    ;ldh  [hLinkInteractiveMotionBlocked], a 

RandomTeleportPositions:
    db $55, $54, $54, $54, $55, $55, $55, $54, $65, $55, $54, $65, $56, $56, $55, $55
    db $55, $45, $65, $54, $55, $55, $55, $55, $55, $55, $55, $58, $43, $57, $55, $55
    db $55, $55, $55, $55, $55, $54, $55, $53, $54, $56, $65, $65, $56, $55, $57, $65
    db $45, $55, $55, $55, $55, $55, $55, $55, $48, $45, $43, $34, $35, $35, $36, $34
    db $65, $55, $55, $54, $54, $54, $55, $54, $56, $65, $55, $55, $55, $55, $54, $54
    db $55, $55, $55, $55, $56, $55, $55, $54, $55, $55, $55, $53, $45, $35, $53, $46
    db $56, $55, $55, $55, $53, $55, $54, $54, $55, $55, $55, $54, $44, $55, $55, $54
    db $55, $55, $45, $55, $55, $54, $45, $45, $63, $55, $65, $55, $45, $45, $44, $54
    db $56, $56, $54, $55, $54, $55, $55, $55, $55, $55, $55, $56, $54, $55, $65, $56
    db $54, $54, $55, $65, $56, $54, $55, $56, $55, $55, $55, $66, $65, $65, $55, $56
    db $65, $55, $55, $75, $55, $55, $55, $54, $55, $55, $65, $57, $55, $54, $53, $45
    db $55, $56, $55, $55, $55, $45, $54, $55, $54, $55, $56, $55, $55, $55, $55, $54
    db $55, $55, $65, $55, $55, $54, $53, $58, $55, $05, $58, $55, $55, $55, $74, $55
    db $55, $55, $55, $55, $46, $55, $55, $56, $55, $55, $55, $54, $55, $45, $55, $55
    db $55, $55, $54, $55, $55, $55, $65, $55, $55, $46, $55, $55, $56, $55, $55, $55
    db $55, $55, $54, $55, $55, $55, $45, $36, $53, $51, $57, $53, $56, $54, $45, $46
