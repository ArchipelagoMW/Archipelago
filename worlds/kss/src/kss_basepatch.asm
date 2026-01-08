;norom
;org $5FFFFF
;    db $FF

;org $407FC0 ; copy header
;    dd read4($7FC0)
;    dd read4($7FC4)
;    dd read4($7FC8)
;    dd read4($7FCC)
;    dd read4($7FD0)
;    dd read4($7FD4)
;    dd read4($7FD8)
;    dd read4($7FDC)
;    dd read4($7FE0)
;    dd read4($7FE4)
;    dd read4($7FE8)
;    dd read4($7FEC)
;    dd read4($7FF0)
;    dd read4($7FF4)
;    dd read4($7FF8)
;    dd read4($7FFC)

;org $7FD7
;db $0D ; 33Mbit~64Mbit
;org $407FD7
;db $0D ; 33MBit~64Mbit

sa1rom

; SNES hardware registers
!VMADDL = $002116
!VMDATAL = $002118
!MDMAEN = $00420B
!DMAP0 = $004300
!BBAD0 = $004301
!A1T0L = $004302
!A1B0 = $004304
!DAS0L = $004305

; Menu select bitflag
; This is not initially a bitflag, we are converting it
; b00000001 - Spring Breeze
; b00000010 - Dyna Blade
; b00000100 - Gourmet Race
; b00001000 - The Great Cave Offensive
; b00010000 - Revenge of Meta Knight
; b00100000 - Milky Way Wishes
; b01000000 - The Arena
; b10000000 - Sound Test (use as completion flag?)
!spring_breeze = #$0000
!dyna_blade = #$0001
!gourmet_race = #$0002
!great_cave_offensive = #$0003
!revenge_of_meta_knight = #$0004
!milky_way_wishes = #$0005
!the_arena = #$0006
!sound_test = #$0007
!samurai_kirby = #$0008
!megaton_punch = #$0009
!stereo = #$000A
!no_sub_game = #$00FF

; Menu Directions
!up = #$0000
!right = #$0001
!down = #$0002
!left = #$0003

; Game variables
!current_revenge_chapter = $7A69
!received_sub_games = $7A85
!current_selected_sub_game = $7A91
!completed_sub_games = $7A93
!great_cave_treasures = $7B05
!great_cave_gold = $7B0F
!received_copy_abilities = $7B1D ; Milky Way Wishes Deluxe Copy Essence, 3-bytes
!rainbow_hearts = $7A6B

; AP save variables
!ap_sub_games = $408000
!received_items = $408002
!received_planets = $408004
!play_sfx = $408006
!activate_candy = $408008
!mirror_game = $40800A
!mirror_room = $40800C


org $008C29
    JSL WriteBWRAM
    NOP
    NOP

org $00910C
    JSL MainLoop

org $00BD44
hook_soft_reset:
    JSL soft_reset
    NOP
    NOP
    NOP

org $00C3EA
always_check_dyna:
    CMP #$0007


org $00C406
hook_dyna_clear:
    JSL dyna_clear
    NOP #4


org $00C46F
hook_set_star_complete:
    JML set_star_complete
    hook_set_star_return:

org $00FFC0
    db "KSS__BASEPATCH_ARCHI"

org $00FFD8
    db $07

org $01922E
    JML block_tgco_access
    tgco_access_return:
    NOP #2

org $01FA1F
    JSL great_cave_requirement
    NOP

org $02A34B
    JML hook_copy_ability
    NOP

org $059810
    JML hook_maxim_tomato
    NOP

org $07DEB2
    NOP #3 ; Grants the initial treasure of TGCO for some reason, probably for the tutorial?

org $07DF3B
    NOP #6 ; Dyna Blade initialization, just need to preserve switch state

org $07DF95
    JSL load_game
    NOP #14 ; TGCO initialization

org $07E01F
    NOP #12 ; Milky Way Wishes initialization

org $C7F98E
EssenceLookup:
    dw $000, $300, $600, $900, $C00, $F00, $1200, $1500, $1800, $1B00, $1E00, $2100, $2400, $2700, $2A00, $2D00
    dw $3000, $3300, $3600, $3900, $3C00, $3F00, $4200, $4500, $4800, $4B00, $4E00, $5100, $5400, $5700, $5A00, $5D00
    dw $6000, $6300, $6600, $6900, $6C00, $6F00, $7200, $7500, $7800, $7B00, $7E00, $8100, $8400, $8700, $8A00, $8D00
    dw $9000, $9300, $9600, $9900, $9C00, $9F00, $A200, $A500, $A800, $AB00, $AE00, $B100, $B400, $B700, $BA00, $BD00

SetEntityFlagX:
    PHA
    PHY
    PHX
    TXA
    JSR SetEntityFlag
    PLX
    PLY
    PLA
    RTL

SetEntityFlagY:
    PHA
    PHY
    PHX
    TYA
    JSR SetEntityFlag
    PLX
    PLY
    PLA
    RTL

SetEntityFlag:
    ; Everything is saved, don't worry about restoring values
    TAX
    LDA $738E
    BEQ .Return
    LDA #$00FF
    STZ $14
    STA $16
    LDA #$000C
    CLC
    ADC $32EC
    TAY
    LDA [$14], Y
    LDY #$00C7
    STY $16
    LDY.w #EssenceLookup
    STY $14
    CLC
    ADC $32F0
    SEC
    SBC #$0022
    TAY
    LDA [$14], Y
    STA $14
    LDA $32F4
    ASL
    CLC
    ADC $14
    PHA
    ; Now we need to get our offset and mask
    LDA $7936, X
    DEC
    TAX
    LDY #$0000
    .Loop:
    CPX #$0008
    BMI .Continue
    INY
    TXA
    SEC
    SBC #$0008
    TAX
    BRA .Loop
    .Continue:
    LDA #$0001
    .Mask:
    CPX #$0000
    BEQ .Set
    ASL
    DEX
    BRA .Mask
    .Set:
    STY $14
    TAX
    PLA
    CLC
    ADC $14
    TAY
    TXA
    PHB
    PHA
    LDA #$4141
    PHA
    PLB
    PLB
    PLA
    ORA $0000, Y
    STA $0000, Y
    PLB
    .Return
    RTS

hook_maxim_tomato:
    LDA $32EA
    CMP #$0006
    BEQ .ArenaMaxim
    LDA $7573
    BEQ .Maxim
    JML $05981E
    .Maxim:
    print "Maxims: ", hex(snestopc(realbase()))
    LDA #$0000
    BNE .Continue
    .DoMaxim:
    LDA $28
    CMP $737A, Y
    BEQ .Full
    JML $059815
    .Full:
    JML $059843
    .Continue:
    LDY $39
    JSL SetEntityFlagY
    JML $059840
    .ArenaMaxim:
    print "Arena Maxims: ", hex(snestopc(realbase()))
    LDA #$0000
    BNE .Continue
    BRA .DoMaxim

hook_one_up:
    print "OneUp: ", hex(snestopc(realbase()))
    LDA #$0000
    BNE .Continue
    INC $737A
    BRA .Return
    .Continue:
    JSL SetEntityFlagY
    .Return
    ; cursed stack magic
    PLA
    PLB
    PHA
    LDA #$0000
    PHA
    PLB
    PLB
    JML $CF79C6

hook_invincibility_candy:
    print "Candy: ", hex(snestopc(realbase()))
    LDA #$0000
    BNE .Continue
    STX $7575
    LDA #$FFFF
    JML $CF6E9A
    .Continue:
    JSL SetEntityFlagY
    JML $CF6EDC

org $CA8532
    JML set_dyna_switch
    NOP #2 ; we don't really care about these, but lets let it be recoverable

org $CAA6F8
    JML block_mww_planets
    NOP 

org $CAB682
handle_menu_remap:
    LDA #$0000
    CLC
    ADC $00
    TAY
    LDA !current_selected_sub_game
    ASL
    TAX
    LDA.l remap_table, X
    STA $14
    LDA #$00CA
    STA $16
    JML [$3714]
    menu_return:
    NOP

org $CAB86E
    JML set_starting_stage
    NOP #49

org $CAB8AA
    LDA #$0005

org $CABCD6
    JML subgame_requirement_visual

org $CAF830
remap_table:
    dw remap_spring_breeze
    dw remap_dyna_blade
    dw remap_gourmet_race
    dw remap_great_cave
    dw remap_meta_knight
    dw remap_milky_way_wishes
    dw remap_arena
    dw remap_sound_test
    dw remap_samurai
    dw remap_megaton
    dw remap_stereo

check_level_access:
    PHA
    PHX
    TAX
    LDA #$0001
    .Loop:
    CPX #$0000
    BEQ .Test
    ASL
    DEX
    BRA .Loop
    .Test:
    AND !received_sub_games
    BNE .ReturnTrue
    CLC
    BRA .Return
    .ReturnTrue:
    SEC
    .Return:
    PLX
    PLA
    RTS

remap_spring_breeze:
    CPY !left
    BEQ .ReturnFalse
    CPY !up
    BEQ .ReturnFalse
    CPY !right
    BEQ .Right
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    LDA !stereo
    BRA .Return
    .Right:
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

remap_dyna_blade:
    CPY !left
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    CPY !down
    BEQ .Down
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Up:
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Down:
    LDA !stereo
    BRA .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

remap_gourmet_race:
    CPY !up
    BEQ .ReturnFalse
    CPY !left
    BEQ .Left
    CPY !down
    BEQ .Down
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Down:
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !stereo
    BRA .Return
    .Left:
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

remap_great_cave:
    CPY !up
    BEQ .Up
    CPY !right
    BEQ .Right
    CPY !left
    BEQ .Left
    ; Down
    LDA !stereo
    BRA .Return
    .Up:
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Right:
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Left:
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_meta_knight:
    CPY !up
    BEQ .Up
    CPY !right
    BEQ .Right
    CPY !left
    BEQ .Left
    LDA !megaton_punch
    BRA .Return
    .Up:
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Right:
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Left:
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_milky_way_wishes:
    CPY !up
    BEQ .ReturnFalse
    CPY !right
    BEQ .ReturnFalse
    CPY !left
    BEQ .Left
    .Down:
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Left:
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_arena:
    CPY !down
    BEQ .ReturnFalse
    CPY !right
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    LDA !samurai_kirby
    BRA .Return
    .Up:
    ; Only check MWW and Revenge, check others on Stereo so menu access is safe
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_sound_test:
    CPY !down
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    CPY !right
    BEQ .Right
    LDA !stereo
    BRA .Return
    .Right:
    LDA !megaton_punch
    BRA .Return
    .Up
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_megaton:
    CPY !left
    BEQ .Left
    CPY !up
    BEQ .Up
    LDA !samurai_kirby
    BRA .Return
    .Left:
    LDA !sound_test
    JSR check_level_access
    BCS .Return
    LDA !stereo
    BRA .Return
    .Up
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_samurai:
    CPY !down
    BEQ .ReturnFalse
    CPY !right
    BEQ .Right
    LDA !megaton_punch
    BRA .Return
    .Right:
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_stereo:
    CPY !down
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    CPY !left
    BEQ .Left
    LDA !sound_test
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Up:
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Left:
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

determine_treasure:
    ; mostly a copy of 00EA71
    ; but we can't use it because of JSL
    LDX #$0022
    .Find:
    DEX
    DEX
    CMP $00EA8E, X
    BCC .Find
    TXY
    AND #$0007
    TAX
    TYA
    LSR
    TAY
    LDA #$0001
    .Loop:
    DEX
    BMI .Return
    ASL
    BRA .Loop
    .Return:
    RTS

check_treasure:
    STX $14
    LDX #$0040
    STX $16
    JSR determine_treasure
    AND [$14], Y
    STA $28
    RTL

set_treasure:
    STX $14
    LDX #$0040
    STX $16
    ;// quick return if game mode == 2
    LDX $7390
    CPX #$0002
    BEQ .Return
    JSR determine_treasure
    ORA [$14], Y
    STA [$14], Y
    .Return:
    RTL

hook_copy_ability:
    PHY
    PHX
    PHA
    LDA $746D, X
    AND #$00FF ; ability items are 0x80XX, need to mask off the flag
    LDY #$0000
    SEC
    SBC #$0001
    .Loop1:
    CMP #$0008
    BCC .CheckLoop
    INY
    SEC
    SBC #$0008
    BRA .Loop1
    .CheckLoop:
    TAX
    LDA #$0001
    .Loop2:
    CPX #$0000
    BEQ .CheckCopy
    ASL
    DEX
    BRA .Loop2
    .CheckCopy:
    AND !received_copy_abilities, Y
    BEQ .NoAbility
    PLA
    PLX
    PLY
    CMP #$0005
    BNE .Return
    JML $02A350
    .NoAbility:
    PLA
    PLX
    PLY
    LDA #$0000
    STZ $746D, X
    STZ $7471, X
    .Return
    JML $02A37E

WriteBWRAM:
    LDA #$1EFE
    MVN $00, $00
    PHB
    LDX #$0000
    LDY #$0014
    .LoopHead:
    LDA $408100, X ; rom header
    CMP $FFC0, X ; compare to real rom name
    BNE .InitializeRAM ; area is uninitialized or corrupt, reset
    INX
    DEY
    BMI .Return ; if Y is negative, rom header matches, valid bwram
    BRA .LoopHead ; else continue loop
    .InitializeRAM:
    LDA #$0000
    STA $402000
    LDX #$2000
    LDY #$2001
    LDA #$EFFE
    MVN $40, $40
    LDA #$0000
    STA $410000
    LDX #$0000
    LDY #$0001
    LDA #$FFFE
    MVN $41, $41
    LDX #$FD00 ; seed info 0x3D000
    LDY #$9000 ; target location
    LDA #$0300
    MVN $40, $07
    LDX #$FFC0 ; ROM name
    LDY #$8100 ; target
    LDA #$0015
    MVN $40, $00
    .Return:
    PLB
    RTL

block_mww_planets:
    CMP #$0008
    BEQ .ReturnSpecial
    PHA
    PHX
    TAX
    LDA #$0001
    .Loop:
    CPX #$0000
    BEQ .Check
    ASL
    DEX
    BRA .Loop
    .Check:
    AND !received_planets
    BEQ .ReturnFalse
    PLX
    PLA
    JML $CAA70C
    .ReturnSpecial:
    JML $CAA6FD
    .ReturnFalse:
    PLX
    PLA
    LDA #$0008
    STA $6D56, X
    JML $CAA72C

block_ability_essence:
    PHY
    PHX
    PHA
    JSL SetEntityFlagY
    LDY #$0000
    SEC
    SBC #$0001
    .Loop1:
    CMP #$0008
    BCC .CheckLoop
    INY
    SEC
    SBC #$0008
    BRA .Loop1
    .CheckLoop:
    TAX
    LDA #$0001
    .Loop2:
    CPX #$0000
    BEQ .CheckCopy
    ASL
    DEX
    BRA .Loop2
    .CheckCopy:
    AND !received_copy_abilities, Y
    BEQ .PullNoAbility
    PLA
    PLX
    PLY
    BNE .Return
    .PullNoAbility:
    PLA
    PLX
    PLY
    .NoAbility:
    JML $CF7699
    .Return
    CMP $749F
    BEQ .NoAbility
    JML $CF76A4

set_dyna_switch:
    LDA $407A64
    AND #$00FF
    STA $28
    LDA $7A77
    ORA $28
    SEP #$20
    STA $407A64
    REP #$20
    STZ $7A77
    RTL

set_starting_stage:
    PHY
    PHX
    LDA #$0001
    LDX #$0007
    LDY #$0000
    .CompletionLoop:
    CPX #$0000
    BEQ .SetStarting
    BIT !completed_sub_games
    BEQ .NotComplete
    INY
    .NotComplete:
    DEX
    ASL
    BRA .CompletionLoop
    .SetStarting:
    print "Starting Stage: ", hex(snestopc(realbase()))
    LDA #$0001
    PHA
    PHA
    .GoalNumeric:
    print "Goal Numeric Requirement: ", hex(snestopc(realbase()))
    CPY #$0006
    BCC .SkipPull
    LDA !completed_sub_games
    .GoalSpecific:
    print "Goal Specific Requirements: ", hex(snestopc(realbase()))
    AND #$007F
    CMP #$007F
    BNE .SkipPull
    LDA #$0041
    JSL $00D003
    PLA
    ORA #$0080
    BRA .Skip
    .SkipPull:
    PLA
    .Skip:
    ORA !ap_sub_games
    STA !received_sub_games
    PLA
    LDX #$0000
    .Loop:
    BIT #$0001
    BNE .Break
    INX
    LSR
    BRA .Loop
    .Break:
    STX $7A91
    STX $7A87
    PLY
    PLX
    RTL

soft_reset:
    JSL save_game
    LDA #$0000
    JSL $00D12D
    RTL

TreasureRequirements:
    print "Treasures: ", hex(snestopc(realbase()))
    dd $2625A0, $4C4B40, $7270E0, $989676

block_tgco_access:
    LDA $32EA
    CMP #$0003
    BNE .Set
    LDA [$14]
    CMP #$000E ; crystal access
    BEQ .Crystal
    CMP #$0013 ; Old Tower access
    BEQ .OldTower
    CMP #$003A ; Garden access
    BEQ .Garden
    CMP #$0035 ; Exit access
    BEQ .Exit
    BRA .Set
    .SetWithPull:
    PLB
    .Set:
    LDA #$0002
    STA $332A
    JML tgco_access_return
    .Crystal:
    LDY #$0002
    BRA .check_treasure
    .OldTower
    LDY #$0006
    BRA .check_treasure
    .Garden:
    LDY #$000A
    BRA .check_treasure
    .Exit:
    LDY #$000E
    .check_treasure:
    PHB
    LDA #$CA00
    PHA
    PLB
    LDX #$0002
    LDA !great_cave_gold, X
    PLB
    CMP TreasureRequirements, Y
    BCC .Block
    BNE .SetWithPull ; branch if greater not equal
    DEX #2
    DEY #2
    LDA #$CA00
    PHA
    PLB
    LDA !great_cave_gold, X
    PLB
    CMP TreasureRequirements, Y
    BCC .Block ; if not minus at this point, has to be greater or equal
    BRA .SetWithPull
    .Block:
    PLB
    LDY #$0002
    LDA $6986, Y
    STA $330C
    LDA $6A00, Y
    STA $3310
    JML $019254

set_star_complete:
    JSL set_treasure
    print "MWW Mode: ", hex(snestopc(realbase()))
    LDA #$0000
    BNE .Return
    LDA $407A6B
    STA $401A6B
    .Return:
    JML hook_set_star_return

invincibility_candy:
    LDX #$0002
    STX $7575
    LDA #$FFFF
    STA $7573
    LDA #$0078
    STA $7571
    LDA #$000A
    STA $35EF, X
    LDA #$0438
    STA $35F3, X
    LDA #$0200
    STA $74C5, X
    TXY
    LDA #$0000
    LDX #$88C6
    JSL $03D6B9
    LDA #$AE11
    JSL $05AC5F
    LDA #$002C
    JSL $00D12D
    LDA #$0014
    JSL $00D003
    RTL

MainLoop:
    JSL $009258
    PHX
    LDA !play_sfx
    BEQ .Candy
    JSL $00D12D
    LDA #$0000
    STA !play_sfx
    .Candy:
    LDA !activate_candy
    BEQ .Mirror
    JSL invincibility_candy
    LDA #$0000
    STA !activate_candy
    .Mirror:
    LDA $32EA
    STA !mirror_game
    LDA $32F2
    STA !mirror_room
    .Return:
    PLX
    RTL

credits_goal_check:
    JSL $00D003 ; start credits music
    LDA #$0001
    LDX #$0007
    LDY #$0000
    .CompletionLoop:
    CPX #$0000
    BEQ .CheckGoal
    BIT !completed_sub_games
    BEQ .NotComplete
    INY
    .NotComplete:
    DEX
    ASL
    BRA .CompletionLoop
    .CheckGoal:
    TYA
    CMP.l set_starting_stage_GoalNumeric+1
    BCC .Return
    LDA !completed_sub_games
    AND.l set_starting_stage_GoalSpecific+1
    CMP.l set_starting_stage_GoalSpecific+1
    BNE .Return
    LDA !received_sub_games
    ORA #$0080
    STA !received_sub_games
    .Return:
    RTL

great_cave_requirement:
    REP #$20
    INC $00B1
    LDA $32EA
    CMP #$0003
    BNE .NoPull
    LDY #$FFFE
    PHB
    .CheckRequirementHigh:
    INY #2
    INY #2
    CPY #$000F
    BPL .EarlyReturn ; we have enough to clear
    LDA #$CA00
    PHA
    PLB
    LDX #$0002
    LDA !great_cave_gold, X
    PLB
    CMP TreasureRequirements, Y
    BCC .GetDigitsHigh
    BNE .CheckRequirementHigh ; branch if greater not equal
    DEX #2
    DEY #2
    LDA #$CA00
    PHA
    PLB
    LDA !great_cave_gold, X
    PLB
    CMP TreasureRequirements, Y
    BCC .GetDigits ; if not minus at this point, has to be greater or equal
    INY #2
    BRA .CheckRequirementHigh
    .EarlyReturn:
    PLB
    .NoPull:
    RTL
    .GetDigits:
    INY #2
    .GetDigitsHigh:
    TYX
    LDA TreasureRequirements, X
    TAY
    DEX #2
    LDA TreasureRequirements, X
    TAX
    LDA #$4040
    PHA
    PLB
    PLB
    TXA
    CPY #$0098
    BCC .Start
    BNE .SetCap
    CMP #$967F
    BCC .Start
    .SetCap:
    LDA #$967F
    LDY #$0098
    .Start
    STA $A001
    LDX #$FFFF
    .Millions:
    INX
    LDA $A001
    SEC
    SBC #$4240
    STA $A001
    TYA
    SBC #$000F
    TAY
    BPL .Millions
    SEP #$20
    TXA
    STA $A000
    REP #$20
    LDA $A001
    CLC
    ADC #$4240
    STA $A001
    TYA
    ADC #$000F
    TAY
    LDA $A001
    LDX #$FFFF
    .HundredThousands:
    INX
    SEC
    SBC #$86A0
    BCS .HTContinue
    DEY
    .HTContinue:
    DEY
    BPL .HundredThousands
    STX $A001
    CLC
    ADC #$86A0
    BCC .AddOne
    INY
    .AddOne:
    INY
    LDX #$FFFF
    .TenThousands:
    INX
    SEC
    SBC #$2710
    BCS .TenThousands
    DEY
    BPL .TenThousands
    STX $A002
    ADC #$2710
    LDX #$FFFF
    SEC
    .Thousands:
    INX
    SBC #$03E8
    BCS .Thousands
    STX $A003
    ADC #$03E8
    LDX #$FFFF
    SEC
    .Hundreds:
    INX
    SBC #$0064
    BCS .Hundreds
    STX $A004
    ADC #$0064
    LDX #$FFFF
    SEC
    .Tens:
    INX
    SBC #$000A
    BCS .Tens
    STX $A005
    ADC #$000A
    STA $A006
    .FindFirstNonZero:
    LDY #$FFFF
    .NonZeroLoop:
    INY
    CPY #$0006
    BEQ .Continue
    SEP #$20
    LDA $A000, Y
    REP #$20
    BEQ .NonZeroLoop
    .Continue:
    STY $A007
    .Apply:
    LDY #$001F
    LDX #$0000
    LDA #$0040
    PHA
    PHA
    PHA
    PHA
    PHA
    PHA
    PHA
    SEP #$20
    .ApplyLoop:
    PLB
    LDA $A000, X
    CPX $A007
    BPL .Add
    LDA #$FF
    BRA .Set
    .Add:
    CLC
    ADC #$B6
    .Set:
    PLB
    STA ($14), Y
    LDA $171B, Y
    STA $173B, Y
    INY
    INX
    CPX #$0007
    BMI .ApplyLoop
    REP #$20
    PLB
    RTL

subgame_requirement_visual:
    MVN $7E, $7E
    .SetVisuals:
    ; insane how the timing for this works out
    LDA #$7ECA
    PHA
    PLB
    LDX set_starting_stage_GoalSpecific+1
    PLB
    LDY #$0000
    .VisualLoop:
    TXA
    BIT #$0001
    BEQ .VisualSkip
    LDA #$1E1D
    STA $7494, Y
    INY
    INY
    BRA .VisualContinue
    .VisualSkip:
    INY
    INY
    .VisualContinue:
    TXA
    LSR
    BEQ .Return
    TAX
    BRA .VisualLoop
    .Return:
    LDA #$7ECA
    PHA
    PLB
    LDA set_starting_stage_GoalNumeric+1
    PLB
    CLC
    ADC #$02CF
    STA $73B8
    LDA #$1E1D
    STA $73B6
    PLB
    JML $CABCDA

dyna_clear:
    LDA #$0001
    LDX $02
    DEX
    .Loop:
    BEQ .Continue
    ASL
    DEX
    BRA .Loop
    .Continue:
    ORA $407A63
    STA $407A63
    LDA #$0009
    RTL

org $CEE9C4
hook_credits:
    JSL credits_goal_check

org $CF2933
remove_dyna_block:
    LDA #$0000

org $CF3FB1
hook_check_treasure:
    JSL check_treasure

org $CF4372
hook_set_treasure_value:
    ; we don't actually care about this value, just remove it
    NOP #22

org $CF44BD
hook_set_treasure:
    JSL set_treasure

org $CF6C7A
one_up:
    JSL hook_one_up
    NOP #2

org $CF6E94
consumable_candy:
    JML hook_invincibility_candy
    NOP #2

org $CF71EB
check_deluxe_ability:
    JSL check_treasure

org $CF73B1
hook_deluxe_ability:
    JSL set_treasure
    NOP #3 ; this is the item count increase

org $CF7694
hook_ability_essence:
    JML block_ability_essence
    NOP

org $CFAA16
remap_deluxe_essence:
    db $00, $00, $01, $02, $03, $04, $05, $06, $07, $08, $09, $0A, $0B, $0C, $0D, $0E, $0F, $10, $11, $12

org $D1BF9D
save_game:

org $D1BFD6
load_game: