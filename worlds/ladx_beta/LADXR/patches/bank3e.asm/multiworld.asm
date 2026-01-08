; Handle the multiworld link

MainLoop:
    ; Check if the gameplay is world
    ld   a, [$DB95]
    cp   $0B
    jr   nz, .clearSafeAndRet
    ; Check if the world subtype is the normal one
    ld   a, [$DB96]
    cp   $07
    jr   nz, .clearSafeAndRet
    ; Check if we are moving between rooms
    ld   a, [$C124]
    and  a
    jr   nz, .clearSafeAndRet
    ; Check if link is in a normal walking/swimming state
    ld   a, [$C11C]
    cp   $02
    jr   nc, .clearSafeAndRet
    ; Check if a dialog is open
    ld   a, [$C19F]
    and  a
    jr   nz, .clearSafeAndRet
    ; Check if interaction is blocked
    ldh  a, [$FFA1]
    and  a
    jr   z, .gameplayIsSafe
.clearSafeAndRet:
    xor  a
    ld   [wConsecutiveSafe], a
    ret

.gameplayIsSafe:
    ; Store consecutive safe frames, up to overflow
    ld   a, [wConsecutiveSafe]
    inc  a
    jr   z, .checkSpawnDelay
    ld   [wConsecutiveSafe], a

.checkSpawnDelay:
    ld   a, [wLinkSpawnDelay]
    and  a
    jr   z, .spawnThings
    dec  a
    ld   [wLinkSpawnDelay], a
    jr   .deathLink ; no spawn

.spawnThings:
    ld   a, [wZolSpawnCount]
    and  a
    call nz, LinkSpawnSlime
    ld   a, [wCuccoSpawnCount]
    and  a
    call nz, LinkSpawnCucco
    ld   a, [wDropBombSpawnCount]
    and  a
    call nz, LinkSpawnBomb

.deathLink:
    ld   hl, wMWCommand
    bit  7, [hl] ; no commands happen if bit 7 is unset
    ret  z
    bit  3, [hl] ; check for death link
    jr   z, .collect
    ; require an arbitrary number of consecutive safe frames to kill the player
    ; the goal is to avoid killing a player after they give up a trade item
    ; but before they get the item in return
    ld   a, [wConsecutiveSafe]
    cp   $10
    ret  c
    ld   a, [wHasMedicine]
    ; set health and health loss to a
    ; instant kill if no medicine
    ; kill with damage if medicine (to trigger medicine)
    ld   [$DB5A], a ; wHealth
    ld   [$DB94], a ; wSubtractHealthBuffer
    ; set health gain to zero
    xor  a
    ld   [$DB93], a ; wAddHealthBuffer

.collect:
    ld   hl, wMWCommand
    bit  2, [hl]
    jr   z, .giveItem
    ; get current location value onto b
    ld   a, [wMWMultipurposeC] ; collect location hi
    ld   h, a
    ld   a, [wMWMultipurposeD] ; collect location lo
    ld   l, a
    ldh  a, [$FFF6] ; current room
    cp   l
    jr   z, .clearCmdAndRet ; might be in current room
    ld   a, [hl]
    ld   b, a
    ld   a, [wMWMultipurposeE] ; location mask
    or   b ; apply mask
    cp   b ; was location already set?
    jr   z, .clearCmdAndRet ; if so, do nothing else
    ld   [hl], a

.giveItem:
    ; Have an item to give?
    ld   hl, wMWCommand
    bit  0, [hl]
    jr   z, .clearCmdAndRet
    ld   hl, wMWCommand
    bit  1, [hl] ; do recvindex check only if bit set
    jr   z, .skipRecvIndexCheck
    ld   a, [wMWRecvIndexHi]
    ld   b, a
    ld   a, [wMWMultipurposeC]
    cp   b
    jr   nz, .clearCmdAndRet ; failed check on hi
    ld   a, [wMWRecvIndexLo]
    ld   b, a
    ld   a, [wMWMultipurposeD]
    cp   b
    jr   nz, .clearCmdAndRet ; failed check on lo
    ; increment recvindex
    ld   a, [wMWRecvIndexLo]
    inc  a
    ld   [wMWRecvIndexLo], a
    jr   nz, .skipRecvIndexCheck ; no overflow, done
    ld   a, [wMWRecvIndexHi]
    inc  a
    ld   [wMWRecvIndexHi], a

.skipRecvIndexCheck:
    ; clear command
    xor  a
    ld   hl, wMWCommand
    ld   [hl], a
    ; Give an item to the player
    ld   a, [wMWItemCode]
    ; if zol:
    cp   $22 ; zol item
    jr   z, LinkGiveSlime
    ; if special item
    cp   $F0
    jr   nc, HandleSpecialItem
    ; tmpChestItem = a
    ldh  [$FFF1], a
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
    ld   a, $C9
    ; OpenDialog()
    jp   $2385 ; Opendialog in $000-$0FF range

.clearCmdAndRet:
    ; check if trade item should be cleared
    ; get mask loaded
    ld   a, [wMWMultipurposeF]
    ld   b, a

    ; check trade 1
    ld   hl, wMWCommand
    bit  4, [hl]
    jr   z, .checkTrade2
    ld   a, [wTradeSequenceItem]
    and  b
    ld   [wTradeSequenceItem], a

.checkTrade2:
    ld   hl, wMWCommand
    bit  5, [hl]
    jr   z, .actuallyClearCmdAndRet
    ld   a, [wTradeSequenceItem2]
    and  b
    ld   [wTradeSequenceItem2], a

.actuallyClearCmdAndRet:
    res  7, [hl]
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
    ldh  [$FFBD], a
    ldh  [$FFBF], a
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
    ldh  a, [$FF98]
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    ldh  a, [$FF99]
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

