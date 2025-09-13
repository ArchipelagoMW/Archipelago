fullsa1rom

!GAME_STATUS = $36D0

; SNES hardware registers
!VMADDL = $002116
!VMDATAL = $002118
!MDMAEN = $00420B
!DMAP0 = $004300
!BBAD0 = $004301
!A1T0L = $004302
!A1B0 = $004304
!DAS0L = $004305

org $008033
    JSL WriteBWRAM
    NOP #5

org $00A245
HSVPatch:
  BRA .Jump
  PHX
  LDA $6CA0,X
  TAX
  LDA $6E22,X
  JSR $A25B
  PLX
  INX
  .Jump:
  JSL HeartStarVisual


org $00A3FC
    JSL NintenHalken
    NOP

org $00EAE4
    JSL MainLoopHook
    NOP

org $00F85E
    JSL SpeedTrap
    NOP #2

org $00FFC0
    db "KDL3_BASEPATCH_ARCHI"

org $00FFD8
    db $06

org $018405
    JSL PauseMenu

org $01AFC8
    JSL HeartStarCheck
    NOP #13

org $01B013
    SEC ; Remove Dedede Bad Ending

org $01B050
    JSL HookBossPurify
    NOP

org $02B7B0 ; Zero unlock
    LDA $80A0
    CMP #$0001

org $02C238
    LDA #$0006
    JSL OpenWorldUnlock
    NOP #5

org $02C27C
    JSL HeartStarSelectFix
    NOP #2

org $02C317
    JSL LoadFont

org $02C39D
    JSL StageCompleteSet
    NOP #2

org $02C3D9
    JSL StrictBosses
    NOP #2

org $02C3F0
    JSL OpenWorldBossUnlock
    NOP #6

org $02C463
    JSL NormalGoalSet
    NOP #2

org $049CD7
    JSL AnimalFriendSpawn

org $06801E
    JSL ConsumableSet

org $068518
    JSL CopyAbilityOverride
    NOP #2

org $099F35
    JSL HeartStarCutsceneFix

org $09A01F
    JSL HeartStarGraphicFix
    NOP #2
    db $B0

org $09A0AE
    JSL HeartStarGraphicFix
    NOP #2
    db $90

org $0A87E8
    JSL CopyAbilityAnimalOverride
    NOP #2

org $12B238
    JSL FinalIcebergFix
    NOP #10
    db $B0

org $14A3EB
    LDA $07A2, Y
    JSL StarsSet
    NOP #3

org $15BC13
    JML GiftGiving
    NOP

org $0799A0
CopyAbilityOverride:
    LDA $54F3, Y
    PHA
    ASL
    TAX
    PLA
    CMP $8020, X
    NOP #2
    BEQ .StoreAbilityK
    LDA #$0000
    .StoreAbilityK:
    STA $54A9, Y
    RTL
    NOP #4
CopyAbilityAnimalOverride:
    PHA
    ASL
    TAY
    PLA
    CMP $8020, Y
    NOP
    BEQ .StoreAbilityA
    LDA #$0000
    .StoreAbilityA:
    STA $54A9, X
    STA $39DF, X
    RTL

HeartStarCheck:
    TXA
    CMP #$0000 ; is this level 1
    BEQ .PassToX
    LSR
    LSR
    INC
    .PassToX:
    TAX
    LDA $8070 ; heart stars
    CLC
    CMP $07D00A ;Compare to goal heart stars
    BCC .CompareWorldHS ; we don't have enough
    PHX
    LDA #$0014
    STA $7F62 ; play sound fx 0x14
    LDA $07D012 ; goal
    CMP #$0000 ; are we on zero goal?
    BEQ .ZeroGoal ; we are
    LDA #$0001
    LDX $3617 ; current save
    STA $53DD, X ; boss butch
    STA $53DF, X ; MG5
    STA $53E1, X ; Jumping
    BRA .PullX
    .ZeroGoal:
    LDA #$0001
    STA $80A0 ; zero unlock address
    .PullX:
    PLX
    .CompareWorldHS:
    LDA $8070 ; current heart stars
    CMP $07D000, X ; compare to world heart stars
    BCS .ReturnTrue
    CLC
    RTL
    .ReturnTrue:
    SEC
    RTL

OpenWorldUnlock:
    PHX
    LDX $900E ; Are we on open world?
    BNE .Open ; Branch if we are
    LDA #$0001
    .Open:
    STA $5AC1 ;(cutscene)
    STA $53CD ;(unlocked stages)
    INC
    STA $5AB9 ;(currently selectable stages)
    CPX #$0001
    BNE .Return ; Return if we aren't on open world
    LDA #$0001
    STA $5A9D
    STA $5A9F
    STA $5AA1
    STA $5AA3
    STA $5AA5
    .Return:
    PLX
    RTL

MainLoopHook:
    STA $D4
    INC $3524
    JSL ParseItemQueue
    LDA $7F62 ; sfx to be played
    BEQ .Traps ; skip if 0
    JSL $00D927 ; play sfx
    STZ $7F62
    .Traps:
    LDA $36D0
    CMP #$FFFF ; are we in menus?
    BEQ .Return ; return if we are
    LDA $5541 ; gooey status
    BPL .Slowness ; gooey is already spawned
    LDA $39D1 ; is kirby alive?
    BEQ .Slowness ; branch if he isn't
    ; maybe BMI here too?
    LDA $8080
    CMP #$0000 ; did we get a gooey trap
    BEQ .Slowness ; branch if we did not
    JSL GooeySpawn
    DEC $8080
    .Slowness:
    LDA $8082 ; slowness
    BEQ .Eject ; are we under the effects of a slowness trap
    DEC $8082 ; dec by 1 each frame
    .Eject:
    PHX
    PHY
    LDA $54A9 ; copy ability
    BEQ .PullVars ; branch if we do not have a copy ability
    LDA $8084 ; eject ability
    BEQ .PullVars ; branch if we haven't received eject
    LDA #$2000 ; select button press
    STA $60C1 ; write to controller mirror
    DEC $8084
    .PullVars:
    PLY
    PLX
    .Return:
    RTL

HeartStarGraphicFix:
    LDA #$0000
    PHX
    PHY
    LDX $363F ; current level
    LDY $3641 ; current stage
    .LoopLevel:
    CPX #$0000
    BEQ .LoopStage
    INC #6
    DEX
    BRA .LoopLevel ; return to loop head
    .LoopStage:
    CPY #$0000
    BEQ .EndLoop
    INC
    DEY
    BRA .LoopStage ; return to loop head
    .EndLoop
    ASL
    TAX
    LDA $07D080, X ; table of original stage number
    CMP #$0002 ; is the current stage a minigame stage?
    BEQ .ReturnTrue ; branch if so
    CLC
    BRA .Return
    .ReturnTrue:
    SEC
    .Return:
    PLY
    PLX
    RTL

ParseItemQueue:
; Local item queue parsing
    NOP
    LDX #$0000
    .LoopHead:
    LDA $C000,X
    BIT #$0010
    BNE .Ability
    BIT #$0020
    BNE .Animal
    BIT #$0040
    BNE .Positive
    BIT #$0080
    BNE .Negative
    .LoopCheck:
    INX
    INX
    CPX #$000F
    BCC .LoopHead
    RTL
    .Ability:
    JSL .ApplyAbility
    RTL
    .Animal:
    JSL .ApplyAnimal
    RTL
    .Positive:
    LDY $36D0
    CPY #$FFFF
    BEQ .LoopCheck
    JSL .ApplyPositive
    RTL
    .Negative:
    AND #$000F
    ASL
    TAY
    JSL .ApplyNegative
    RTL
    .ApplyAbility:
    AND #$000F
    PHA
    ASL
    TAY
    PLA
    STA $8020,Y
    LDA #$0032
    BRA .PlaySFX
    .ApplyAnimal:
    AND #$000F
    PHA
    ASL
    TAY
    PLA
    INC
    STA $8000,Y
    LDA #$0032
    BRA .PlaySFX
    .PlaySFX:
    STA $7F62
    STZ $C000,X
    .Return:
    RTL
    .ApplyPositive:
    LDY $36D0
    CPY #$FFFF
    BEQ .Return
    AND #$000F
    BEQ .HeartStar
    CMP #$0004
    BCS .StarBit
    CMP #$0002
    BCS .Not1UP
    LDA $39CF
    INC
    STA $39CF
    STA $39E3
    LDA #$0033
    BRA .PlaySFX
    .Not1UP:
    CMP #$0003
    BEQ .Invincibility
    LDA $39D3
    BEQ .JustKirby
    LDA #$0008
    STA $39D1
    STA $39D3
    BRA .PlayPositive
    .JustKirby:
    LDA #$000A
    STA $39D1
    BRA .PlayPositive
    .Invincibility:
    LDA #$0384
    STA $54B1
    BRA .PlayPositive
    .HeartStar:
    INC $8070
    LDA #$0016
    BRA .PlaySFX
    .StarBit:
    SEC
    SBC #$0004
    ASL
    INC
    CLC
    ADC $39D7
    ORA #$8000
    STA $39D7
    .PlayPositive:
    LDA #$0026
    .PlaySFXLong
    BRA .PlaySFX
    .ApplyNegative:
    CPY #$0005
    BCS .PlayNone
    LDA $8080,Y
    CPY #$0002
    BNE .Increment
    CLC
    LDA #$0384
    ADC $8080, Y
    BVC .PlayNegative
    LDA #$FFFF
    .PlayNegative:
    STA $8080,Y
    LDA #$00A7
    BRA .PlaySFXLong
    .Increment:
    INC
    STA $8080, Y
    BRA .PlayNegative
    .PlayNone:
    LDA #$0000
    BRA .PlaySFXLong

AnimalFriendSpawn:
    PHA
    CPX #$0002  ; is this an animal friend?
    BNE .Return
    XBA
    PHA
    PHX
    PHA
    LDX #$0000
    .CheckSpawned:
    LDA $05CA, X
    BNE .Continue
    LDA #$0002
    CMP $074A, X
    BNE .ContinueCheck
    PLA
    PHA
    XBA
    CMP $07CA, X
    BEQ .AlreadySpawned
    .ContinueCheck:
    INX
    INX
    BRA .CheckSpawned
    .Continue:
    PLA
    PLX
    ASL
    TAY
    PLA
    INC
    CMP $8000, Y ; do we have this animal friend
    BEQ .Return ; we have this animal friend
    .False:
    INX
    .Return:
    PLY
    LDA #$9999
    RTL
    .AlreadySpawned:
    PLA
    PLX
    ASL
    TAY
    PLA
    BRA .False


WriteBWRAM:
    LDY #$6001 ;starting addr
    LDA #$1FFE ;bytes to write
    MVN $40, $40 ;copy $406000 from 406001 to 407FFE
    LDX #$0000
    LDY #$0014
    .LoopHead:
    LDA $8100, X ; rom header
    CMP $07C000, X ; compare to real rom name
    BNE .InitializeRAM ; area is uninitialized or corrupt, reset
    INX
    DEY
    BMI .Return ; if Y is negative, rom header matches, valid bwram
    BRA .LoopHead ; else continue loop
    .InitializeRAM:
    LDA #$0000
    STA $8000 ; initialize first byte that gets copied
    LDX #$8000
    LDY #$8001
    LDA #$7FFD
    MVN $40, $40 ; initialize 0x8000 onward
    LDX #$D000 ; seed info 0x3D000
    LDY #$9000 ; target location
    LDA #$1000
    MVN $40, $07
    LDX #$C000 ; ROM name
    LDY #$8100 ; target
    LDA #$0015
    MVN $40, $07
    .Return:
    RTL

ConsumableSet:
    PHA
    PHX
    PHY
    AND #$00FF
    PHA
    LDX $53CF
    LDY $53D3
    LDA #$0000
    DEY
    .LoopLevel:
    CPX #$0000
    BEQ .LoopStage
    CLC
    ADC #$0007
    DEX
    BRA .LoopLevel ; return to loop head
    .LoopStage:
    CPY #$0000
    BEQ .EndLoop
    INC
    DEY
    BRA .LoopStage ; return to loop head
    .EndLoop:
    ASL
    TAX
    LDA $07D020, X ; current stage
    ASL #6
    TAX
    PLA
    .LoopHead:
    CMP #$0000
    BEQ .ApplyCheck
    INX
    DEC
    BRA .LoopHead ; return to loop head
    .ApplyCheck:
    LDA $A000, X ; consumables index
    PHA
    ORA #$0001
    STA $A000, X
    PLA
    AND #$00FF
    BNE .Return
    TXA
    ORA #$1000
    JSL ApplyLocalCheck
    .Return:
    PLY
    PLX
    PLA
    XBA
    AND #$00FF
    RTL

NormalGoalSet:
    PHX
    LDA $07D012
    CMP #$0000
    BEQ .ZeroGoal
    LDA #$0001
    LDX $3617 ; current save
    STA $53DD, X ; Boss butch
    STA $53DF, X ; MG5
    STA $53D1, X ; Jumping
    BRA .Return
    .ZeroGoal:
    LDA #$0001
    STA $80A0
    .Return:
    PLX
    LDA #$0006
    STA $5AC1 ; cutscene
    RTL

FinalIcebergFix:
    PHX
    PHY
    LDA #$0000
    LDX $363F
    LDY $3641
    .LoopLevel:
    CPX #$0000
    BEQ .LoopStage
    INC #7
    DEX
    BRA .LoopLevel ; return to loop head
    .LoopStage:
    CPY #$0000
    BEQ .CheckStage
    INC
    DEY
    BRA .LoopStage ; return to loop head
    .CheckStage:
    ASL
    TAX
    LDA $07D020, X
    CMP #$001D
    BEQ .ReturnTrue
    CLC
    BRA .Return
    .ReturnTrue:
    SEC
    .Return:
    PLY
    PLX
    RTL

StrictBosses:
    PHX
    LDA $901E ; Do we have strict bosses enabled?
    BEQ .ReturnTrue ; Return True if we don't, always unlock the boss in this case
    LDA $53CB ; unlocked level
    CMP #$0005 ; have we unlocked level 5?
    BCS .ReturnFalse ; we don't need to do anything if so
    NOP #5 ;unsure when these got here
    LDX $53CB
    DEX
    TXA
    ASL
    TAX
    LDA $8070 ; current heart stars
    CMP $07D000, X ; do we have enough HS to purify?
    BCS .ReturnTrue ; branch if we do
    .ReturnFalse:
    SEC
    BRA .Return
    .ReturnTrue:
    CLC
    .Return:
    PLX
    LDA $53CD
    RTL

NintenHalken:
    LDX #$0005
    .Halken:
    LDA $00A405, X ; loop head (halken)
    STA $4080F0, X
    DEX
    BPL .Halken ; branch if more letters to copy
    LDX #$0005
    .Ninten:
    LDA $00A40B, X ; loop head (ninten)
    STA $408FF0, X
    DEX
    BPL .Ninten ; branch if more letters to copy
    REP #$20
    LDA #$0001
    RTL

StageCompleteSet:
    PHX
    LDA $5AC1 ; completed stage cutscene
    BEQ .Return ; we have not completed a stage
    LDA #$0000
    LDX $53CF ; current level
    .LoopLevel:
    CPX #$0000
    BEQ .StageStart
    DEX
    INC #7
    BRA .LoopLevel ; return to loop head
    .StageStart:
    LDX $53D3 ; current stage
    CPX #$0007 ; is this a boss stage
    BEQ .Return ; return if so
    DEX
    .LoopStage:
    CPX #$0000
    BEQ .LoopEnd
    INC
    DEX
    BRA .LoopStage ; return to loop head
    .LoopEnd:
    ASL
    TAX
    LDA $9020, X ; load the stage we completed
    ASL
    TAX
    PHX
    LDA $8200, X
    AND #$00FF
    BNE .ApplyClear
    TXA
    LSR
    JSL ApplyLocalCheck
    .ApplyClear:
    PLX
    LDA #$0001
    ORA $8200, X
    STA $8200, X
    .Return:
    PLX
    LDA $53CF
    CMP $53CB
    RTL

OpenWorldBossUnlock:
    PHX
    PHY
    LDA $900E ; Are we on open world?
    BEQ .ReturnTrue ; Return true if we aren't, always unlock boss
    LDA $53CD
    CMP #$0006
    BNE .ReturnFalse ; return if we aren't on stage 6
    LDA $53CF
    INC
    CMP $53CB ; are we on the most unlocked level?
    BNE .ReturnFalse ; return if we aren't
    LDA #$0000
    LDX $53CF
    .LoopLevel:
    CPX #$0000
    BEQ .LoopStages
    ADC #$0006
    DEX
    BRA .LoopLevel ; return to loop head
    .LoopStages:
    ASL
    TAX
    LDA #$0000
    LDY #$0006
    PHY
    PHX
    .LoopStage:
    PLX
    LDY $9020, X ; get stage id
    INX
    INX
    PHA
    TYA
    ASL
    TAY
    PLA
    ADC $8200, Y ; add current stage value to total
    PLY
    DEY
    PHY
    PHX
    CPY #$0000
    BNE .LoopStage ; return to loop head
    PLX
    PLY
    SEC
    SBC $9016
    BCC .ReturnFalse
    .ReturnTrue
    LDA $53CD
    INC
    STA $53CD
    STA $5AC1
    BRA .Return
    .ReturnFalse:
    STZ $5AC1
    .Return:
    PLY
    PLX
    RTL

GooeySpawn:
    PHY 
    PHX 
    LDX #$0000
    LDY #$0000
    STA $5543
    LDA $1922,Y
    STA $C0
    LDA $19A2,Y
    STA $C2
    LDA #$0008
    STA $C4
    LDA #$0002
    STA $352A
    LDA #$0003
    JSL $00F54F
    STX $5541
    LDA #$FFFF
    STA $0622,X
    JSL $00BAEF
    JSL $C4883C
    LDX $39D1
    CPX #$0001
    BEQ .Return
    LDA #$FFFF
    CPX #$0002
    BEQ .Call
    DEC 
    .Call:
    JSL $C43C22
    .Return:
    PLX 
    PLY 
    RTL 

SpeedTrap:
    PHX
    LDX $8082 ; do we have slowness
    BEQ .Apply ; branch if we do not
    LSR
    .Apply:
    PLX
    STA $1F22, Y ; player max speed
    EOR #$FFFF
    RTL

HeartStarVisual:
    CPX #$0000
    BEQ .SkipInx
    INX
    .SkipInx
    CPX $651E
    BCC .Return
    CPX #$0000
    BEQ .Return
    LDA $4036D0
    AND #$00FF
    BEQ .ReturnTrue
    LDA $3000
    AND #$0200
    CMP #$0000
    BNE .ReturnTrue
    PHY
    LDA $3000
    TAY
    CLC
    ADC #$0020
    STA $3000
    LDA $408070
    LDX #$0000
    .LoopHead:
    CMP #$000A
    BCC .LoopEnd
    SEC
    SBC #$000A
    INX
    BRA .LoopHead
    .LoopEnd:
    PHX
    TAX
    PLA
    ORA #$2500
    PHA
    LDA #$2C70
    STA $0000, Y
    PLA
    INY
    INY
    STA $0000, Y
    INY
    INY
    TXA
    ORA #$2500
    PHA
    LDA #$2C78
    STA $0000, Y
    INY
    INY
    PLA
    STA $0000, Y
    INY
    INY
    JSL HeartStarVisual2 ; we ran out of room
    PLY
    .ReturnTrue:
    SEC
    .Return:
    RTL

LoadFont:
    JSL $00D29F ; play sfx
    PHX
    PHB
    LDA #$0000
    PHA
    PLB
    PLB
    LDA #$7000
    STA $2116
    LDX #$0000
    .LoopHead:
    CPX #$0140
    BEQ .LoopEnd
    LDA $D92F50, X
    STA $2118
    INX
    INX
    BRA .LoopHead
    .LoopEnd:
    LDX #$0000
    .2LoopHead:
    CPX #$0020
    BEQ .2LoopEnd
    LDA $D92E10, X
    STA $2118
    INX
    INX
    BRA .2LoopHead
    .2LoopEnd:
    PHY
    LDA $07D012
    ASL
    TAX
    LDA $07E000, X
    TAX
    LDY #$0000
    .3LoopHead:
    CPY #$0020
    BEQ .3LoopEnd
    LDA $D93170, X
    STA $2118
    INX
    INX
    INY
    INY
    BRA .3LoopHead
    .3LoopEnd:
    LDA $07D00C
    ASL
    TAX
    LDA $07E010, X
    TAX
    LDY #$0000
    .4LoopHead:
    CPY #$0020
    BEQ .4LoopEnd
    LDA $D93170, X
    STA $2118
    INX
    INX
    INY
    INY
    BRA .4LoopHead
    .4LoopEnd:
    PLY
    PLB
    PLX
    RTL

HeartStarVisual2:
    LDA #$2C80
    STA $0000, Y
    INY
    INY
    LDA #$250A
    STA $0000, Y
    INY
    INY
    LDA $4053CF
    ASL
    TAX
    .LoopHead:
    LDA $409000, X
    CMP #$FFFF
    BNE .LoopEnd
    DEX
    DEX
    BRA .LoopHead
    .LoopEnd:
    LDX #$0000
    .2LoopHead:
    CMP #$000A
    BCC .2LoopEnd
    SEC
    SBC #$000A
    INX
    BRA .2LoopHead ; return to loop head
    .2LoopEnd:
    PHX
    TAX
    PLA
    ORA #$2500
    PHA
    LDA #$2C88
    STA $0000, Y
    PLA
    INY
    INY
    STA $0000, Y
    INY
    INY
    TXA
    ORA #$2500
    PHA
    LDA #$2C90
    STA $0000, Y
    INY
    INY
    PLA
    STA $0000, Y
    INY
    INY
    LDA #$14D8
    STA $0000, Y
    INY
    INY
    LDA #$250B
    STA $0000, Y
    INY
    INY
    LDA #$14E0
    STA $0000, Y
    INY
    INY
    LDA #$250A
    STA $0000, Y
    INY
    INY
    LDA #$14E8
    STA $0000, Y
    INY
    INY
    LDA #$250C
    STA $0000, Y
    INY
    INY
    LDA $3000
    SEC
    SBC #$3040
    LSR
    LSR
    .3LoopHead:
    CMP #$0004
    BCC .3LoopEnd
    DEC #4
    BRA .3LoopHead ; return to loop head
    .3LoopEnd:
    STA $3240
    LDA #$0004
    SEC
    SBC $3240
    TAX
    LDA #$00FF
    .4LoopHead:
    CPX #$0000
    BEQ .4LoopEnd
    LSR
    LSR
    DEX
    BRA .4LoopHead
    .4LoopEnd:
    LDY $3002
    AND $0000, Y
    STA $0000, Y
    INY
    LDA #$0000
    STA $0000, Y
    INY
    INY
    STA $0000, Y
    RTL

HeartStarSelectFix:
    PHX
    TXA
    ASL
    TAX
    LDA $9020, X
    TAX
    .LoopHead:
    CMP #$0006
    BMI .LoopEnd
    INX
    SEC
    SBC #$0006
    BRA .LoopHead
    .LoopEnd:
    LDA $53A7, X
    PLX
    AND #$00FF
    RTL

HeartStarCutsceneFix:
    TAX
    LDA $53D3
    DEC
    STA $5AC3
    LDA $53A7, X
    AND #$00FF
    BNE .Return
    PHX
    TXA
    .Loop:
    CMP #$0007
    BCC .Continue
    SEC
    SBC #$0007
    DEX
    BRA .Loop
    .Continue:
    TXA
    ORA #$0100
    JSL ApplyLocalCheck
    PLX
    .Return
    RTL

GiftGiving:
    CMP #$0008
    .This:
    BCS .This  ; this intentionally safe-crashes the game if hit
    PHX
    LDX $901C
    BEQ .Return
    PLX
    STA $8086
    LDA #$0026
    JML $CABC99
    .Return:
    PLX
    JML $CABC18

PauseMenu:
    JSL $00D29F
    PHX
    PHY
    LDA #$3300
    STA !VMADDL
    LDA #$0007
    STA !A1B0
    LDA #$F000
    STA !A1T0L
    LDA #$01C0
    STA !DAS0L
    SEP #$20
    LDA #$01
    STA !DMAP0
    LDA #$18
    STA !BBAD0
    LDA #$01
    STA !MDMAEN
    REP #$20
    LDY #$0000
    .LoopHead:
    INY ; loop head
    CPY #$0009
    BPL .LoopEnd
    TYA
    ASL
    TAX
    LDA $8020, X
    BEQ .LoopHead ; return to loop head
    TYA
    CLC
    ADC #$31E2
    STA !VMADDL
    LDA $07E020, X
    STA !VMDATAL
    BRA .LoopHead ; return to loop head
    .LoopEnd:
    LDY #$FFFF
    .2LoopHead:
    INY ; loop head
    CPY #$0007
    BPL .2LoopEnd
    TYA
    ASL
    TAX
    LDA $8000, X
    BEQ .2LoopHead ; return to loop head
    TYA
    CLC
    ADC #$3203
    STA !VMADDL
    LDA $07E040, X
    STA !VMDATAL
    BRA .2LoopHead ; return to loop head
    .2LoopEnd:
    PLY
    PLX
    RTL

StarsSet:
    PHA
    PHX
    PHY
    LDX $901A
    BEQ .ApplyStar
    AND #$00FF
    PHA
    LDX $53CF
    LDY $53D3
    LDA #$0000
    DEY
    .LoopLevel:
    CPX #$0000
    BEQ .LoopStage
    CLC
    ADC #$0007
    DEX
    BRA .LoopLevel
    .LoopStage:
    CPY #$0000
    BEQ .LoopEnd
    INC
    DEY
    BRA .LoopStage
    .LoopEnd:
    ASL
    TAX
    LDA $07D020, X
    ASL
    ASL
    ASL
    ASL
    ASL
    ASL
    TAX
    PLA
    .2LoopHead:
    CMP #$0000
    BEQ .2LoopEnd
    INX
    DEC
    BRA .2LoopHead
    .2LoopEnd:
    LDA $B000, X
    PHA
    ORA #$0001
    STA $B000, X
    PLA
    AND #$00FF
    BNE .Return
    TXA
    ORA #$2000
    JSL ApplyLocalCheck
    .Return:
    PLY
    PLX
    PLA
    XBA
    AND #$00FF
    RTL
    .ApplyStar:
    LDA $39D7
    INC
    ORA #$8000
    STA $39D7
    BRA .Return

ApplyLocalCheck:
; args: A-address of check following $08B000
    TAX
    LDA $09B000, X
    AND #$00FF
    TAY
    LDX #$0000
    .Loop:
    LDA $C000, X
    BEQ .Apply
    INX
    INX
    CPX #$0010
    BCC .Loop
    BRA .Return ; this is dangerous, could lose a check here
    .Apply:
    TYA
    STA $C000, X
    .Return:
    RTL

HookBossPurify:
    ORA $B0
    STA $53D5
    LDA $B0
    LDX #$0000
    LSR
    .Loop:
    BIT #$0001
    BNE .Apply
    LSR
    LSR
    INX
    CPX #$0005
    BCS .Return
    BRA .Loop
    .Apply:
    TXA
    ORA #$0200
    JSL ApplyLocalCheck
    .Return:
    RTL

org $07C000
    db "KDL3_BASEPATCH_ARCHI"

org $07E000
    db $20, $03
    db $20, $00
    db $80, $01
    db $20, $01
    db $00, $00
    db $00, $00
    db $00, $00
    db $00, $00
    db $A0, $01
    db $A0, $00

; Pause Icons

org $07E020
    db $00, $0C
    db $30, $09
    db $31, $09
    db $32, $09
    db $33, $09
    db $34, $09
    db $35, $09
    db $36, $09
    db $37, $09

org $07E040
    db $38, $05
    db $39, $05
    db $3A, $01
    db $3B, $05
    db $3C, $05
    db $3D, $05

org $07F000
incbin "APPauseIcons.dat"