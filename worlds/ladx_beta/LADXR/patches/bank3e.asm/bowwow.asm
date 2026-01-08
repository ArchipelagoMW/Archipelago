CheckIfLoadBowWow:
        ; Check has bowwow flag
        ld   a, [$DB56]
        cp   $01
        jr   nz, .noLoadBowwow

        ldh  a, [$FFF6] ; load map number
        cp   $22
        jr   z, .loadBowwow
        cp   $23
        jr   z, .loadBowwow
        cp   $24
        jr   z, .loadBowwow
        cp   $32
        jr   z, .loadBowwow
        cp   $33
        jr   z, .loadBowwow
        cp   $34
        jr   z, .loadBowwow

.noLoadBowwow:
        ld   e, $00
        ret

.loadBowwow:
        ld   e, $01
        ret


; Special handler for when Bowwow tries to eat an entity.
; Our target entity index is loaded in BC.
BowwowEat:
    ; Load the entity type into A
    ld   hl, $C3A0 ; entity type
    add  hl, bc
    ld   a, [hl]

    ; Check if we need special handling for bosses
    cp   $59 ; Moldorm
    jr   z, BowwowHurtEnemy
    cp   $5C ; Genie
    jr   z, BowwowEatGenie
    cp   $5B ; SlimeEye
    jp   z, BowwowEatSlimeEye
    cp   $65 ; AnglerFish
    jr   z, BowwowHurtEnemy
    cp   $5D ; SlimeEel
    jp   z, BowwowEatSlimeEel
    cp   $5A ; Facade
    jr   z, BowwowHurtEnemy
    cp   $63 ; Eagle
    jr   z, BowwowHurtEnemy
    cp   $62 ; Hot head
    jp   z, BowwowEatHotHead
    cp   $F9 ; Hardhit beetle
    jr   z, BowwowHurtEnemy
    cp   $E6 ; Nightmare (all forms)
    jp   z, BowwowEatNightmare

    ; Check for special handling for minibosses
    cp   $87 ; Lanmola
    jr   z, BowwowHurtEnemy
    ; cp   $88 ; Armos knight
    ; No special handling, just eat him, solves the fight real quick.
    cp   $81 ; rolling bones
    jr   z, BowwowHurtEnemy
    cp   $89 ; Hinox
    jr   z, BowwowHurtEnemy
    cp   $8E ; Cue ball
    jr   z, BowwowHurtEnemy
    ;cp   $5E ; Gnoma
    ;jr   z, BowwowHurtEnemy
    cp   $5F ; Master stalfos
    jr   z, BowwowHurtEnemy
    cp   $92 ; Smasher
    jp   z, BowwowEatSmasher
    cp   $BC ; Grim Creeper
    jp   z, BowwowEatGrimCreeper
    cp   $BE ; Blaino
    jr   z, BowwowHurtEnemy
    cp   $F8 ; Giant buzz blob
    jr   z, BowwowHurtEnemy
    cp   $F4 ; Avalaunch
    jr   z, BowwowHurtEnemy

    ; Some enemies
    cp   $E9 ; Color dungeon shell
    jr   z, BowwowHurtEnemy
    cp   $EA ; Color dungeon shell
    jr   z, BowwowHurtEnemy
    cp   $EB ; Color dungeon shell
    jr   z, BowwowHurtEnemy

    ; Play SFX
    ld   a, $03
    ldh  [$FFF2], a
    ; Call normal "destroy entity and drop item" handler
    jp   $3F50

BowwowHurtEnemy:
    ; Hurt enemy with damage type zero (sword)
    ld   a, $00
    ld   [$C19E], a
    rst  $18
    ; Play SFX
    ld   a, $03
    ldh  [$FFF2], a
    ret

BowwowEatGenie:
    ; Get private state to find out if this is a bottle or the genie
    ld   hl, $C2B0
    add  hl, bc
    ld   a, [hl]
    ; Prepare loading state from hl
    ld   hl, $C290
    add  hl, bc

    cp   $00
    jr   z, .bottle
    cp   $01
    jr   z, .ghost
    ret

.ghost:
    ; Get current state
    ld   a, [hl]
    cp   $04 ; Flying around without bottle
    jr   z, BowwowHurtEnemy
    ret

.bottle:
    ; Get current state
    ld   a, [hl]
    cp   $03 ; Hopping around in bottle
    jr   z, BowwowHurtEnemy
    ret

BowwowEatSlimeEye:
    ; On set privateCountdown2 to $0C to split, when privateState1 is $04 and state is $03
    ld   hl, $C290 ; state
    add  hl, bc
    ld   a, [hl]
    cp   $03
    jr   nz, .skipSplit

    ld   hl, $C2B0 ; private state1
    add  hl, bc
    ld   a, [hl]
    cp   $04
    jr   nz, .skipSplit

    ld   hl, $C300 ; private countdown 2
    add  hl, bc
    ld   [hl], $0C

.skipSplit:
    jp   BowwowHurtEnemy

BowwowEatSlimeEel:
    ; Get private state to find out if this is the tail or the head
    ld   hl, $C2B0
    add  hl, bc
    ld   a, [hl]
    cp   $01  ; not the head, so, skip.
    ret  nz

    ; Check if we are pulled out of the wall
    ld   hl, $C290
    add  hl, bc
    ld   a, [hl]
    cp   $03  ; pulled out of the wall
    jr   nz, .knockOutOfWall

    ld   hl, $D204
    ld   a, [hl]
    cp   $07
    jr   nc, .noExtraDamage
    inc  [hl]
.noExtraDamage:
    jp   BowwowHurtEnemy

.knockOutOfWall:
    ld   [hl], $03 ; set state to $03
    ld   hl, $C210  ; Y position
    add  hl, bc
    ld   a, [hl]
    ld   [hl], $60
    cp   $48
    jp   nc, BowwowHurtEnemy
    ld   [hl], $30
    jp   BowwowHurtEnemy


BowwowEatHotHead:
    ; Load health of hothead
    ld   hl, $C360
    add  hl, bc
    ld   a, [hl]
    cp   $20
    jr   c, .lowHp
    ld   [hl], $20
.lowHp:
    jp   BowwowHurtEnemy

BowwowEatSmasher:
    ; Check if this is the ball or the monster
    ld   hl, $C440
    add  hl, bc
    ld   a, [hl]
    and  a
    ret  nz
    jp   BowwowHurtEnemy

BowwowEatGrimCreeper:
    ; Check if this is the main enemy or the smaller ones. Only kill the small ones
    ld   hl, $C2B0
    add  hl, bc
    ld   a, [hl]
    and  a
    ret  z
    jp   BowwowHurtEnemy

BowwowEatNightmare:
    ; Check if this is the staircase.
    ld   hl, $C390
    add  hl, bc
    ld   a, [hl]
    cp   $02
    ret  z

    ; Prepare loading state from hl
    ld   hl, $C290
    add  hl, bc

    ld   a, [$D219] ; which form has the nightmare
    cp   $01
    jr   z, .slimeForm
    cp   $02
    jr   z, .agahnimForm
    cp   $03 ; moldormForm
    jp   z, BowwowHurtEnemy
    cp   $04 ; ganon and lanmola
    jp   z, BowwowHurtEnemy
    cp   $05 ; dethl
    jp   z, BowwowHurtEnemy
    ; 0 is the intro form
    ret

.slimeForm:
    ld   a, [hl]
    cp   $02
    jr   z, .canHurtSlime
    cp   $03
    ret  nz

.canHurtSlime:
    ; We need quite some custom handling, normally the nightmare checks very directly if you use powder.
    ; No idea why this insta kills the slime form...
    ; Change state to hurt state
    ld   [hl], $07
    ; Set flash count
    ld   hl, $C420
    add  hl, bc
    ld   [hl], $14
    ; play proper sfx
    ld   a, $07
    ldh  [$FFF3], a
    ld   a, $37
    ldh  [$FFF2], a
    ; No idea why this is done, but it happens when you use powder on the slime
    ld   a, $03
    ld   [$D220], a
    ret

.agahnimForm:
    ld   a, [hl]
    ; only damage in states 2 to 4
    cp   $02
    ret  c
    cp   $04
    ret  nc

    ; Decrease health
    ld   a, [$D220]
    inc  a
    ld   [$D220], a
    ; If dead, do stuff
    cp   $04
    jr   c, .agahnimNotDeadYet
    ld   [hl], $07
    ld   hl, $C2E0
    add  hl, bc
    ld   [hl], $C0
    ld   a, $36
    ldh  [$FFF2], a
.agahnimNotDeadYet:
    ld   hl, $C420
    add  hl, bc
    ld   [hl], $14
    ld   a, $07
    ldh  [$FFF3], a
    ret
