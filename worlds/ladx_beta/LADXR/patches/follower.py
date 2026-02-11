from ..assembler import ASM
from ..utils import createTileData


def patchFollowerCreation(rom, *, bowwow_everywhere=False, extra_spawn=""):
    rom.patch(0x01, 0x1FB3, 0x2162, ASM("""
    ; Never spawn in sidescrollers
    ldh  a, [hIsSideScrolling]
    and  a
    ret  nz
    
spawnRooster:
    ld   a, [$DB7B]
    and  a
    jr   z, .end
    ld   a, [wIsIndoor] 
    and  a
    jr   z, .excludedRoomsEnd

    ldh  a, [hMapId] 
    cp   $16 ; MAP_S_FACE_SHRINE 
    jr   z, .end
    cp   $14 ; MAP_KANALET 
    jr   z, .end
    cp   $13 ; MAP_DREAM_SHRINE 
    jr   z, .end
    cp   $FF ; MAP_COLOR_DUNGEON 
    jr   z, .end
    cp   $0A ; all maps below MAP_CAVE_B (includes dungeons) 
    jr   c, .end

.excludedRoomsEnd:
    ld   c, $D5
    call spawnFollowerEntity
.end:

spawnMarin:
    ld   a, [wIsMarinFollowingLink] 
    and  a
    jr   z, .end
    ld   a, [wIsIndoor] 
    and  a
    jr   z, .excludedRoomsEnd

    ldh  a, [hMapId] 
    cp   $16 ; MAP_S_FACE_SHRINE 
    jr   z, .end
    cp   $14 ; MAP_KANALET 
    jr   z, .end
    cp   $13 ; MAP_DREAM_SHRINE 
    jr   z, .end
    cp   $FF ; MAP_COLOR_DUNGEON 
    jr   z, .end
    cp   $0A ; all maps below MAP_CAVE_B (includes dungeons) 
    jr   c, .end

.excludedRoomsEnd:
    ld   c, $C1
    call spawnFollowerEntity

    ; Configure marin, needs some extras
    ldh  a, [hLinkPositionX]
    ld   hl, $D155 ; wLinkPositionXHistory  
    call fillBlock

    ldh  a, [hLinkPositionY]
    ld   hl, $D175 ; wLinkPositionYHistory  
    call fillBlock

    ldh  a, [hLinkPositionZ]
    ld   hl, $D195 ; wLinkPositionZHistory  
    call fillBlock

    ld   hl, wEntitiesPrivateState4Table 
    add  hl, de
    ld   [hl], $01
    ld   hl, wEntitiesPrivateCountdown1Table 
    add  hl, de
    ld   [hl], $0C

.end:

spawnBowwow:
    ld   a, [wIsBowWowFollowingLink] 
    and  a
    jr   z, .end
""" + ("""
    ld   a, [wIsIndoor]
    and  a
    jr   nz, .end

    ldh  a, [hMapRoom]
    cp   $22
    jr   z, .load
    cp   $23
    jr   z, .load
    cp   $24
    jr   z, .load
    cp   $32
    jr   z, .load
    cp   $33
    jr   z, .load
    cp   $34
    jr   nz, .end
""" if not bowwow_everywhere else """

""") + """
.load:

    ld   c, $6D
    call spawnFollowerEntity

    ; Configure marin, needs some extras
    ldh  a, [hLinkPositionX]
    ld   hl, $D155 ; wLinkPositionXHistory  
    call fillBlock

    ldh  a, [hLinkPositionY]
    ld   hl, $D175 ; wLinkPositionYHistory  
    call fillBlock

    ldh  a, [hLinkPositionZ]
    ld   hl, $D195 ; wLinkPositionZHistory  
    call fillBlock

    ld   hl, wEntitiesPrivateState4Table 
    add  hl, de
    ld   [hl], $01
    ld   hl, wEntitiesPrivateCountdown1Table 
    add  hl, de
    ld   [hl], $0C

.end:

""" + ("""
spawnghost:
    ld   c, $D4
    call spawnFollowerEntity
""" if extra_spawn != "" else "") + """
    ret
    
fillBlock:
    ld   c, $10
.loop:
    ldi  [hl], a
    dec  c
    jr   nz, .loop
    ret

spawnFollowerEntity: ; param: c = entity ID 
    ; Search for an existing entity
    ld   e, $0F
    ld   d, $00
.searchLoop:
    ld   hl, wEntitiesTypeTable
    add  hl, de
    ld   a, [hl]
    cp   c ; ENTITY_ID 
    jr   nz, .continue
    ld   hl, wEntitiesStatusTable
    add  hl, de
    ld   a, [hl]
    and  a
    jr   z, .continue
    ld   [hl], d
.continue:
    dec  e
    ld   a, e
    cp   $ff
    jr   nz, .searchLoop

    ld   a, c ; ENTITY_ID
    call SpawnNewEntity_trampoline 

    ; Configure the entity
    ldh  a, [hLinkPositionX]
    ld   hl, wEntitiesPosXTable
    add  hl, de
    ld   [hl], a
    ldh  a, [hLinkPositionY]
    ld   hl, wEntitiesPosYTable
    add  hl, de
    ld   [hl], a
    ldh  a, [hLinkPositionZ]
    ld   hl, wEntitiesPosZTable
    add  hl, de
    ld   [hl], a
    ret
    """, 0x5FB3), fill_nop=True)

    if extra_spawn == "fox":
        patchFoxFollower(rom)
    if extra_spawn == "navi":
        patchNaviFollower(rom)
    if extra_spawn == "ghost":
        patchGhostFollower(rom)
    if extra_spawn == "yipyip":
        patchYipYipFollower(rom)


def patchFoxFollower(rom):
    # Sprite variants
    rom.patch(0x19, 0x1DF8, 0x1E10, ("E609E809" + "E609EA09" + "E829E629" + "EA29E629" + "00000000" + "00000000"))
    # Main entity code
    rom.patch(0x19, 0x1E18, 0x20B3, ASM("""
    DogEntityHandler:
        ; Keep on screen during scrolling
        ldh  a, [$FFF6] ; hMapRoom
        ld   hl, $C3E0 ; wEntitiesRoomTable  
        add  hl, bc
        ld   [hl], a
        ld   hl, $C220 ; wEntitiesPosXSignTable 
        add  hl, bc
        ld   [hl], b
        ld   hl, $C230 ; wEntitiesPosYSignTable 
        add  hl, bc
        ld   [hl], b
        ; Check if we are being burned
        ldh  a, [$FFEA] ; hActiveEntityStatus
        cp   3
        jp   z, onFire
        ; Not being burned, check if we should go into ghost mode
        ld   a, [$DB7A]
        and  a
        jp   nz, ghostMode

        ; Always live
        ld   hl, $C360 ; wEntitiesHealthTable
        add  hl, bc
        ld   [hl], $4C

        ld   hl, $C380 ; wEntitiesDirectionTable
        add  hl, bc
        ld   a, [hl]
        and  a
        jr   nz, .jr_48EE

        ldh  a, [$FFF1] ; hActiveEntitySpriteVariant
        add  $02
        ldh  [$FFF1], a

    .jr_48EE:
        ld   de, $5DF8 ; DogSpriteVariants
        call $3BC0 ; RenderActiveEntitySpritesPair
        call $7D3D ; ReturnIfNonInteractive_19
        call $0C56 ; DecrementEntityIgnoreHitsCountdown
        call $7DF1 ; AddEntityZSpeedToPos_19
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        dec  [hl]
        dec  [hl]
        ld   hl, $C310 ; wEntitiesPosZTable
        add  hl, bc
        ld   a, [hl]
        and  $80
        ldh  [$FFE8], a ; hMultiPurposeG
        jr   z, .jr_4914
        ld   [hl], b
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        ld   [hl], b
    .jr_4914:
        call $3B70
        ld   hl, $C420 ; wEntitiesFlashCountdownTable
        add  hl, bc
        ld   a, [hl]
        and  a
        jr   z, .jr_4963

        cp   $08
        jr   nz, .jr_4963

        call $3B12 ; IncrementEntityState
        ld   a, $02
        ld   [hl], a
        ldh  [$FFF0], a ; hActiveEntityState
        call $0C05 ; GetEntityTransitionCountdown
        ld   [hl], $10

    .jr_4963:

        ldh  a, [$FFF0] ; hActiveEntityState
        rst  0
    ._00: dw DogState0Handler
    ._01: dw DogState1Handler
    ._02: dw DogState2Handler
    ._03: dw DogState3Handler

    Data_RandomSpeed:
        db   $02, $08, $0C, $08
    Data_RandomOffset:
        db   $00, $01, $01, $02, $00, $FF, $FF, $FE

    DogState0Handler:
        xor  a
        call $3B0C ; SetEntitySpriteVariant
        call $0C05 ; GetEntityTransitionCountdown
        jr   nz, .jr_49D8

        ; Move towards link at a random speed
        call $280D ; GetRandomByte
        and  $03
        ld   e, a
        ld   d, b
        ld   hl, Data_RandomSpeed
        add  hl, de
        ld   a, [hl]
        call $3BAA ; ApplyVectorTowardsLink_trampoline

        call $280D ; GetRandomByte
        and  $07
        ld   e, a
        ld   d, b
        ld   hl, Data_RandomOffset
        add  hl, de
        ld   a, [hl]
        ld   hl, $C240 ; wEntitiesSpeedXTable
        add  hl, bc
        add  a, [hl]
        ld   [hl], a
        swap a
        rra
        and  $04
        ld   hl, $C380 ; wEntitiesDirectionTable
        add  hl, bc
        ld   [hl], a
        call $280D ; GetRandomByte
        and  $07
        ld   e, a
        ld   hl, Data_RandomOffset
        add  hl, de
        ld   a, [hl]
        ld   hl, $C250 ; wEntitiesSpeedYTable
        add  hl, bc
        add  a, [hl]
        ld   [hl], a

        call $0C05 ; GetEntityTransitionCountdown
        call $280D ; GetRandomByte
        and  $1F
        add  $30
        ld   [hl], a
        call $3B12 ; IncrementEntityState

    .jr_49D8:
        jp   func_019_49FD

    DogState1Handler:
        call $7DB8 ; UpdateEntityPosWithSpeed_19
        call $3B23
        ldh  a, [$FFE8] ; hMultiPurposeG
        and  a
        jr   z, func_019_49FD

        call $0C05 ; GetEntityTransitionCountdown
        jr   nz, .jr_49F2

        ld   [hl], $18
        call $3B12 ; IncrementEntityState
        ld   [hl], b
        ret

    .jr_49F2:
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        ld   [hl], $08
        ld   hl, $C310 ; wEntitiesPosZTable
        add  hl, bc
        inc  [hl]

    func_019_49FD:
        ldh  a, [$FFE7] ; hFrameCounter
        rra
        rra
        rra
        and  $01
        jp   $3B0C ; SetEntitySpriteVariant

    DogState2Handler:
        call $0C05 ; GetEntityTransitionCountdown
        jr   nz, .jr_4A23

        call $3B12 ; IncrementEntityState
        ld   a, $24
        call $3BAA ; ApplyVectorTowardsLink_trampoline
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        ld   [hl], $18
        call $7E0B ; entityLinkPositionXDifference
        ld   hl, $C380 ; wEntitiesDirectionTable
        add  hl, bc
        ld   a, e
        ld   [hl], a

    .jr_4A23:
        ldh  a, [$FFE7] ; hFrameCounter
        rra
        rra
        and  $01
        jp   $3B0C ; SetEntitySpriteVariant

    DogState3Handler:
        call $7DB8 ; UpdateEntityPosWithSpeed_19
        call $3B23
        ld   hl, $C340 ; wEntitiesPhysicsFlagsTable
        add  hl, bc
        ld   [hl], $52 ; 2 | ENTITY_PHYSICS_SHADOW | ENTITY_PHYSICS_PROJECTILE_NOCLIP
        call $3B44
        ld   hl, $C340 ; wEntitiesPhysicsFlagsTable
        add  hl, bc
        ld   [hl], $92 ; 2 | ENTITY_PHYSICS_SHADOW | ENTITY_PHYSICS_HARMLESS
        ldh  a, [$FFE8] ; hMultiPurposeG
        and  a
        jr   z, .ret_4A4F

        call $3B12 ; IncrementEntityState
        ld   [hl], b
        call $0C05 ; GetEntityTransitionCountdown
        ld   [hl], $20

    .ret_4A4F:
        ret

    onFire:
        ld   hl, $DB7A
        ld   [hl], 6
        ret

    ghostMode:
        ; First check if we should despawn and spawn a few screens later
        dec  a
        jr   z, .active
        ld   [$DB7A], a
        cp   3
        jp   nc, $7E61; ClearEntityStatus_19
        ld   a, $2D ; JINGLE_GHOST_PRESENCE 
        ldh  [$FFF2], a ; hJingle 
        jp   $7E61; ClearEntityStatus_19

    .active:
        ldh  a, [$FFE7] ; hFrameCounter
        add  c 
        and  $01
        jr   nz, .skipDraw
        ld   de, $5DF8 ; DogSpriteVariants
        call $3BC0 ; RenderActiveEntitySpritesPair
    .skipDraw:

        ldh  a, [$FFE7]
        rra
        rra
        rra
        and  $07
        ld   e, a
        ld   d, b
        ld   hl, GhostZPositionTable
        add  hl, de
        ld   a, [hl]
        sub  $04
        ld   hl, $C310 ; wEntitiesPosZTable  
        add  hl, bc
        ld   [hl], a

        call $7E0B ; entityLinkPositionXDifference

        push af
        rlca
        rlca
        and  $02
        xor  $02
        call $3B0C ; SetEntitySpriteVariant    
        pop  af

        add  $18
        cp   $30
        jr   nc, .move

        ldh  a, [hLinkPositionY]
        push af
        add  $0C
        ldh  [$FF99], a ; hLinkPositionY 
        call $7E1B ; entityLinkPositionYDifference  
        ld   e, a
        pop  af
        ldh  [$FF99], a ; hLinkPositionY
        ld   a, e
        add  $18
        cp   $30
        jr   c, .noMove
    .move:

        ld   a, $08
        call $3BAA ; ApplyVectorTowardsLink_trampoline  
        call $7DB8 ; UpdateEntityPosWithSpeed_19

    .noMove:
        ld   a, [$C166] ; wLinkPlayingOcarinaCountdown 
        cp   $01
        jr   nz, .noSong

        ld   a, [$DB49] ; wOcarinaSongFlags
        and  1
        jr   z, .noSong

        ld   a, [$DB4A] ; wSelectedSongIndex 
        cp   $02
        jr   nz, .noSong

        xor  a
        ld   [$DB7A], a

    .noSong:
        ret

    GhostZPositionTable:
        db   $10, $11, $12, $13, $13, $12, $11, $10

    """, 0x5E18), fill_nop=True)

    # Load followers in dungeons, caves, etc
    rom.patch(0x03, 0x03C5, "00", "02")  # ignore in dungeons for kill-all triggers
    rom.patch(0x03, 0x00D4, "d2", "92")  # physics flag
    # Graphics in high VRAM bank
    rom.banks[0x3F][0x3660:0x36C0] = rom.banks[0x32][0x2580:0x25E0]


def patchNaviFollower(rom):
    rom.patch(0x19, 0x1DF8, 0x1E10, ("E80BE82B" + "EA0BEA2B" + "E80BE82B" + "EA0BEA2B" + "E80BE82B" + "EA0BEA2B"))
    rom.patch(0x19, 0x1E18, 0x20B3, ASM("""
GhostEntity:
    ldh  a, [$FFF6] ; hMapRoom
    ld   hl, $C3E0 ; wEntitiesRoomTable  
    add  hl, bc
    ld   [hl], a
    ld   hl, $C220 ; wEntitiesPosXSignTable 
    add  hl, bc
    ld   [hl], b
    ld   hl, $C230 ; wEntitiesPosYSignTable 
    add  hl, bc
    ld   [hl], b

    ldh  a, [$FFE7] ; hFrameCounter 
    rra
    rra
    rra
    and  $07
    ld   e, a
    ld   d, b
    ld   hl, $5E10
    add  hl, de
    ld   a, [hl]
    sub  $0C
    ld   hl, $C310 ; wEntitiesPosZTable 
    add  hl, bc
    ld   [hl], a

    ld   a, [$DB7A]
    cp   $B0
    jr   c, .noDraw
    cp   $F0
    jr   nc, .blink
    cp   $C0
    jr   nc, .draw

.blink:
    ldh  a, [$FFE7] ; hFrameCounter
    and  $2
    jr   z, .noDraw

.draw:
    ld   de, $5DF8 ; GhostSpriteVariants  
    call $3BC0 ; RenderActiveEntitySpritesPair
.noDraw:

    ldh  a, [$FFE7] ; hFrameCounter
    swap a
    and  $01
    call $3B0C ; SetEntitySpriteVariant  

    call $7E0B ; Get X distance with link?
    add  a, $12
    cp   $24
    jr   nc, .moveToLink

    call $7E1B ; Get Y distance with link?
    add  a, $12
    cp   $24
    jr   c, .skipMove

.moveToLink:
    ld   a, $10
    call $3BAA ; ApplyVectorTowardsLink_trampoline  
    call $7DB8 ; UpdateEntityPosWithSpeed_19  

.skipMove:
    call $7D3D ; ReturnIfNonInteractive_19 

    ldh  a, [$FFE7] ; hFrameCounter
    and  $07
    ret  nz

    ld   hl, $DB7A
    inc  [hl]
    ret

""", 0x5E18), fill_nop=True)

    # Load followers in dungeons, caves, etc
    rom.patch(0x03, 0x03C5, "00", "03")  # ignore in dungeons for kill-all triggers

    rom.banks[0x3F][0x3680:0x36C0] = createTileData("""........
........
..11....
..121...
..1231..
..1221..
..12231.
...12233
....1332
.....322
....1322
...12332
..122133
..1111..
........
........
""" + """........
........
........
........
11111...
122311..
13222233
.1322332
..111322
.....322
.....332
....1233
....121.
....131.
.....11.
........""", ".132")


def patchGhostFollower(rom):
    # Sprite variants
    rom.patch(0x19, 0x1DF8, 0x1E10, ("E60BE80B" + "EA0BEC0B" + "E82BE62B" + "EC2BEA2B" + "00000000" + "00000000"))
    # Main entity code
    rom.patch(0x19, 0x1E18, 0x20B3, ASM("""
    GhostEntityHandler:
        ldh  a, [$FFE7] ; hFrameCounter
        swap a
        and  1
        ld   hl, hActiveEntitySpriteVariant
        or   [hl]
        ld   [hl], a

        ldh  a, [$FFE7] ; hFrameCounter
        add  c 
        and  $01
        jr   nz, .skipDraw
        ld   de, $5DF8 ; DogSpriteVariants
        call $3BC0 ; RenderActiveEntitySpritesPair
    .skipDraw:

        ldh  a, [$FFE7]
        rra
        rra
        rra
        and  $07
        ld   e, a
        ld   d, b
        ld   hl, GhostZPositionTable
        add  hl, de
        ld   a, [hl]
        sub  $04
        ld   hl, $C310 ; wEntitiesPosZTable  
        add  hl, bc
        ld   [hl], a

        call $7E0B ; entityLinkPositionXDifference

        push af
        rlca
        rlca
        and  $02
        xor  $02
        call $3B0C ; SetEntitySpriteVariant    
        pop  af

        add  $18
        cp   $30
        jr   nc, .move

        ldh  a, [hLinkPositionY]
        push af
        add  $0C
        ldh  [$FF99], a ; hLinkPositionY 
        call $7E1B ; entityLinkPositionYDifference  
        ld   e, a
        pop  af
        ldh  [$FF99], a ; hLinkPositionY
        ld   a, e
        add  $18
        cp   $30
        jr   c, .noMove
    .move:

        ld   a, $08
        call $3BAA ; ApplyVectorTowardsLink_trampoline  
        call $7DB8 ; UpdateEntityPosWithSpeed_19

    .noMove:
        ret

    GhostZPositionTable:
        db   $10, $11, $12, $13, $13, $12, $11, $10

    """, 0x5E18), fill_nop=True)

    # Load followers in dungeons, caves, etc
    rom.patch(0x03, 0x03C5, "00", "02")  # ignore in dungeons for kill-all triggers
    rom.patch(0x03, 0x00D4, "d2", "92")  # physics flag
    # Graphics in high VRAM bank
    rom.banks[0x3F][0x3660:0x36E0] = rom.banks[0x32][0x1800:0x1880]


def patchYipYipFollower(rom):
    # Sprite variants
    rom.patch(0x19, 0x1DF8, 0x1E10, ("E60AE80A" + "EA0AEC0A" + "E82AE62A" + "EC2AEA2A" + "00000000" + "00000000"))
    # Main entity code
    rom.patch(0x19, 0x1E18, 0x20B3, ASM("""
    YipYipEntityHandler:
        ld   hl, $C360 ; wEntitiesHealthTable
        add  hl, bc
        ld   [hl], $4C

        ld   hl, $C380 ; wEntitiesDirectionTable
        add  hl, bc
        ld   a, [hl]
        and  a
        jr   nz, .jr_48EE

        ldh  a, [$FFF1] ; hActiveEntitySpriteVariant
        add  $02
        ldh  [$FFF1], a

    .jr_48EE:
        ld   de, $5DF8 ; DogSpriteVariants
        call $3BC0 ; RenderActiveEntitySpritesPair
        call $7D3D ; ReturnIfNonInteractive_19
        call $0C56 ; DecrementEntityIgnoreHitsCountdown
        call $7DF1 ; AddEntityZSpeedToPos_19
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        dec  [hl]
        dec  [hl]
        ld   hl, $C310 ; wEntitiesPosZTable
        add  hl, bc
        ld   a, [hl]
        and  $80
        ldh  [$FFE8], a ; hMultiPurposeG
        jr   z, .jr_4914
        ld   [hl], b
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        ld   [hl], b
    .jr_4914:

        ldh  a, [$FFF0] ; hActiveEntityState
        rst  0
    ._00: dw DogState0Handler
    ._01: dw DogState1Handler

    Data_RandomSpeed:
        db   $04, $08, $0C, $08
    Data_RandomOffset:
        db   $00, $01, $01, $02, $00, $FF, $FF, $FE

    DogState0Handler:
        xor  a
        call $3B0C ; SetEntitySpriteVariant
        call $0C05 ; GetEntityTransitionCountdown
        jr   nz, .jr_49D8

        ; Move towards link at a random speed
        call $280D ; GetRandomByte
        and  $03
        ld   e, a
        ld   d, b
        ld   hl, Data_RandomSpeed
        add  hl, de
        ld   a, [hl]
        call $3BAA ; ApplyVectorTowardsLink_trampoline

        call $280D ; GetRandomByte
        and  $07
        ld   e, a
        ld   d, b
        ld   hl, Data_RandomOffset
        add  hl, de
        ld   a, [hl]
        ld   hl, $C240 ; wEntitiesSpeedXTable
        add  hl, bc
        add  a, [hl]
        ld   [hl], a
        swap a
        rra
        and  $04
        ld   hl, $C380 ; wEntitiesDirectionTable
        add  hl, bc
        ld   [hl], a
        call $280D ; GetRandomByte
        and  $07
        ld   e, a
        ld   hl, Data_RandomOffset
        add  hl, de
        ld   a, [hl]
        ld   hl, $C250 ; wEntitiesSpeedYTable
        add  hl, bc
        add  a, [hl]
        ld   [hl], a

        call $0C05 ; GetEntityTransitionCountdown
        call $280D ; GetRandomByte
        and  $1F
        add  $30
        ld   [hl], a
        call $3B12 ; IncrementEntityState

    .jr_49D8:
        jp   func_019_49FD

    DogState1Handler:
        call $7DB8 ; UpdateEntityPosWithSpeed_19
        call $3B23
        ldh  a, [$FFE8] ; hMultiPurposeG
        and  a
        jr   z, func_019_49FD

        call $0C05 ; GetEntityTransitionCountdown
        jr   nz, .jr_49F2

        ld   [hl], $18
        call $3B12 ; IncrementEntityState
        ld   [hl], b
        ret

    .jr_49F2:
        ld   hl, $C320 ; wEntitiesSpeedZTable
        add  hl, bc
        ld   [hl], $08
        ld   hl, $C310 ; wEntitiesPosZTable
        add  hl, bc
        inc  [hl]

    func_019_49FD:
        ldh  a, [$FFE7] ; hFrameCounter
        rra
        rra
        rra
        and  $01
        jp   $3B0C ; SetEntitySpriteVariant

    """, 0x5E18), fill_nop=True)

    # Load followers in dungeons, caves, etc
    rom.patch(0x03, 0x03C5, "00", "02")  # ignore in dungeons for kill-all triggers
    rom.patch(0x03, 0x00D4, "d2", "92")  # physics flag
    rom.patch(0x03, 0x00FB + 0x00D4, "00", "80")  # hitbox flags
    # Graphics in high VRAM bank
    rom.banks[0x3F][0x3660:0x36E0] = rom.banks[0x32][0x2100:0x2180]
