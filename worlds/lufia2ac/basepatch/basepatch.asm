lorom


org $DFFFFD  ; expand ROM to 3MB
    DB "EOF"
org $80FFD8  ; expand SRAM to 16KB
    DB $04                  ; overwrites DB $03

org $80809A  ; patch copy protection
    CMP $704000             ; overwrites CMP $702000
org $8080A6  ; patch copy protection
    CMP $704000             ; overwrites CMP $702000



org $8AEAA3  ; skip gruberik intro dialogue
    DB $1C,$86,$03          ; L2SASM JMP $8AE784+$0386
org $8AEC82  ; skip gruberik save dialogue
    DB $1C,$93,$01          ; L2SASM JMP $8AEB1C+$0193
org $8AECFE  ; skip gruberik abandon dialogue
    DB $1C,$32,$02          ; L2SASM JMP $8AEB1C+$0232
org $8AF4E1  ; skip gruberik selan dialogue
    DB $1C,$D8,$09          ; L2SASM JMP $8AEB1C+$09D8
org $8AF528  ; skip gruberik guy dialogue
    DB $1C,$1E,$0A          ; L2SASM JMP $8AEB1C+$0A1E
org $8AF55F  ; skip gruberik arty dialogue
    DB $1C,$67,$0A          ; L2SASM JMP $8AEB1C+$0A67
org $8AF5B2  ; skip gruberik tia dialogue
    DB $1C,$C3,$0A          ; L2SASM JMP $8AEB1C+$0AC3
org $8AF61A  ; skip gruberik dekar dialogue
    DB $1C,$23,$0B          ; L2SASM JMP $8AEB1C+$0B23
org $8AF681  ; skip gruberik lexis dialogue
    DB $1C,$85,$0B          ; L2SASM JMP $8AEB1C+$0B85

org $8EA349  ; skip ancient cave entrance dialogue
    DB $1C,$B0,$01          ; L2SASM JMP $8EA1AD+$01B0
org $8EA384  ; skip ancient cave exit dialogue
    DB $1C,$2B,$02          ; L2SASM JMP $8EA1AD+$022B
org $8EA565  ; skip ancient cave leaving dialogue
    DB $1C,$E9,$03          ; L2SASM JMP $8EA1AD+$03E9

org $8EA653  ; skip master intro dialogue
    DB $1C,$0F,$01          ; L2SASM JMP $8EA5FA+$010F
org $8EA721  ; skip master fight dialogue
    DB $1C,$45,$01          ; L2SASM JMP $8EA5FA+$0145
org $8EA74B  ; skip master victory dialogue
    DB $1C,$AC,$01          ; L2SASM JMP $8EA5FA+$01AC
org $8EA7AA  ; skip master key dialogue
    DB $1C,$CA,$01          ; L2SASM JMP $8EA5FA+$01CA
org $8EA7F4  ; skip master goodbye dialogue
    DB $1C,$05,$02          ; L2SASM JMP $8EA5FA+$0205
org $8EA807  ; skip master not fight dialogue
    DB $1C,$18,$02          ; L2SASM JMP $8EA5FA+$0218

org $94AC45  ; connect ancient cave exit stairs to gruberik entrance
    DB $67,$09,$18,$68
org $948DE1  ; connect gruberik west border to ancient cave entrance
    DB $07,$08,$14,$F0
org $948DEA  ; connect gruberik south border to ancient cave entrance
    DB $07,$08,$14,$F0
org $948DF3  ; connect gruberik north border to ancient cave entrance
    DB $07,$08,$14,$F0



; archipelago item
org $96F9AD  ; properties
    DB $00,$00,$00,$E4,$00,$00,$00,$00,$00,$00,$00,$00,$00
org $9EDD60  ; name
    DB "AP item     "       ; overwrites "Key30       "
org $9FA900  ; sprite
    incbin "ap_logo/ap_logo.bin"
    warnpc $9FA980


org $D08000  ; signature, start of expanded data area
    DB "ArchipelagoLufia"


org $D09800  ; start of expanded code area



; initialize
pushpc
org $808046
    ; DB=$80, x=1, m=1
    JSL Init                ; overwrites JSL $809037
pullpc

Init:
; check signature
    LDX.b #$0F
-:  LDA $D08000,X
    CMP $F02000,X
    BNE +
    DEX
    BPL -
    BRA ++
; set up DMA to clear expanded SRAM
+:  STZ $211C               ; force multiplication results (MPYx) to zero
    REP #$10
    LDA.b #$80
    STA $4300               ; transfer B-bus to A-bus, with A-bus increment
    LDA.b #$34
    STA $4301               ; B-bus source register $2134 (MPYL)
    LDX.w #$2000
    STX $4302               ; A-bus destination address $F02000 (SRAM)
    LDA.b #$F0
    STA $4304
    STX $4305               ; transfer 8kB
    LDA.b #$01
    STA $420B               ; start DMA channel 1
; sign expanded SRAM
    PHB
    LDA.b #$3F
    LDX.w #$8000
    LDY.w #$2000
    MVN $F0,$D0             ; copy 64B from $D08000 to $F02000
    PLB
++: SEP #$30
    JSL $809037             ; (overwritten instruction)
    RTL



; transmit checks
pushpc
org $8EC1EB
    JML TX                  ; overwrites JSL $83F559
pullpc

TX:
    JSL $83F559             ; (overwritten instruction) chest opening animation
    REP #$20
    LDA $7FD4EF             ; read chest item ID
    BIT.w #$4000            ; test for blue chest flag
    BEQ +
    LDA $F02040             ; load check counter
    CMP $D08010             ; compare against max AP item number
    BPL +
    INC                     ; increment check counter
    STA $F02040             ; store check counter
    SEP #$20
    JML $8EC331             ; skip item get process
+:  SEP #$20
    JML $8EC1EF             ; continue item get process



; report event flag based goal completion
pushpc
org $D09000
    DB $00,$01,$01,$02,$01,$02,$02,$03,$01,$02,$02,$03,$02,$03,$03,$04, \
       $01,$02,$02,$03,$02,$03,$03,$04,$02,$03,$03,$04,$03,$04,$04,$05, \
       $01,$02,$02,$03,$02,$03,$03,$04,$02,$03,$03,$04,$03,$04,$04,$05, \
       $02,$03,$03,$04,$03,$04,$04,$05,$03,$04,$04,$05,$04,$05,$05,$06, \
       $01,$02,$02,$03,$02,$03,$03,$04,$02,$03,$03,$04,$03,$04,$04,$05, \
       $02,$03,$03,$04,$03,$04,$04,$05,$03,$04,$04,$05,$04,$05,$05,$06, \
       $02,$03,$03,$04,$03,$04,$04,$05,$03,$04,$04,$05,$04,$05,$05,$06, \
       $03,$04,$04,$05,$04,$05,$05,$06,$04,$05,$05,$06,$05,$06,$06,$07, \
       $01,$02,$02,$03,$02,$03,$03,$04,$02,$03,$03,$04,$03,$04,$04,$05, \
       $02,$03,$03,$04,$03,$04,$04,$05,$03,$04,$04,$05,$04,$05,$05,$06, \
       $02,$03,$03,$04,$03,$04,$04,$05,$03,$04,$04,$05,$04,$05,$05,$06, \
       $03,$04,$04,$05,$04,$05,$05,$06,$04,$05,$05,$06,$05,$06,$06,$07, \
       $02,$03,$03,$04,$03,$04,$04,$05,$03,$04,$04,$05,$04,$05,$05,$06, \
       $03,$04,$04,$05,$04,$05,$05,$06,$04,$05,$05,$06,$05,$06,$06,$07, \
       $03,$04,$04,$05,$04,$05,$05,$06,$04,$05,$05,$06,$05,$06,$06,$07, \
       $04,$05,$05,$06,$05,$06,$06,$07,$05,$06,$06,$07,$06,$07,$07,$08
pullpc

Goal:
    TDC
    LDA $0797               ; load some event flags (iris sword, iris shield, ..., iris pot)
    TAX
    LDA $0798               ; load some event flags (iris tiara, boss, others...)
    TAY
    AND.b #$02              ; test boss victory
    LSR
    STA $F02031             ; report boss victory goal
    TYA
    AND.b #$01              ; test iris tiara
    ADC $D09000,X           ; test remaining iris items via lookup table
    CMP $D08017             ; compare with number of treasures required
    BMI +
    LDA.b #$01
    STA $F02032             ; report iris treasures goal
    AND $F02031
    STA $F02033             ; report boss victory + iris treasures goal
+:  RTS



; receive items
RX:
    REP #$20
    LDA $F02802             ; load snes side received items processed counter
    CMP $F02800             ; compare with client side received items counter
    BPL +
    INC
    STA $F02802             ; increase received items processed counter
    ASL
    TAX
    LDA $F02802,X           ; load received item ID
    BRA ++
+:  LDA $F02046             ; load snes side found AP items processed counter
    CMP $F02044             ; compare with client side found AP items counter
    BPL +
    LDA $F02044
    STA $F02046             ; increase AP items processed counter
    LDA.w #$01CA            ; load "AP item" ID
++: STA $7FD4EF             ; store it as a "chest"
    JSR SpecialItemGet
    SEP #$20
    JSL $8EC1EF             ; call chest opening routine (but without chest opening animation)
+:  SEP #$20
    RTS

SpecialItemGet:
    BPL +                   ; spells have high bit set
    JSR LearnSpell
+:  CMP.w #$01BF            ; capsule monster items range from $01B8 to $01BE
    BPL +
    SBC.w #$01B1            ; party member items range from $01B2 to $01B7
    BMI +
    ASL
    TAX
    LDA $8ED8C7,X           ; load predefined bitmask with a single bit set
    ORA $F02018             ; set unlock bit for party member/capsule monster
    STA $F02018
+:  RTS

LearnSpell:
    STA $0A0B
    SEP #$20
    LDA.b #$06
-:  PHA
    JSL $82FD3D             ; teach spell in $0A0B to character determined by A
    PLA
    DEC
    BPL -
    REP #$20
    LDA $0A0B
    RTS



; use items
pushpc
org $82AE6F
    ; DB=$83, x=0, m=1
    JSL SpecialItemUse      ; overwrites JSL $81EFDF
org $8EFD2E  ; unused region at the end of bank $8E
    DB $1E,$0B,$01,$2B,$01,$1A,$02,$00  ; add selan
    DB $1E,$0B,$01,$2B,$02,$1A,$03,$00  ; add guy
    DB $1E,$0B,$01,$2B,$03,$1A,$04,$00  ; add arty
    DB $1E,$0B,$01,$2B,$05,$1A,$05,$00  ; add dekar
    DB $1E,$0B,$01,$2B,$04,$1A,$06,$00  ; add tia
    DB $1E,$0B,$01,$2B,$06,$1A,$07,$00  ; add lexis
pullpc

SpecialItemUse:
    JSL $81EFDF             ; (overwritten instruction)
    REP #$20
    LDA $0A06               ; get ID of item being used
    CMP.w #$01B8
    BPL +
    SBC.w #$01B1            ; party member items range from $01B2 to $01B7
    BMI +
    ASL
    ASL
    ASL
    ADC.w #$FD2E
    STA $09B7               ; set pointer to L2SASM join script
    SEP #$20
    LDA $07A9               ; load EV register $11 (party counter)
    CMP.b #$03
    BPL +                   ; abort if party full
    LDA.b #$8E
    STA $09B9
    PHK
    PEA ++
    PEA $8DD8
    JML $83BB76             ; initialize parser variables
++: NOP
    JSL $809CB8             ; call L2SASM parser
    JSL $81F034             ; consume the item
    TSX
    INX #13
    TXS
    JML $82A45E             ; leave menu
+:  SEP #$20
    RTL



; main loop
pushpc
org $83BC16
    ; DB=$83, x=0, m=1
    JSL MainLoop            ; overwrites LDA $09A7 : BIT.b #$01
    NOP
pullpc

MainLoop:
    JSR RX
    JSR Goal
    JSR Unlocks
    LDA $09A7               ; (overwritten instruction)
    BIT.b #$01              ; (overwritten instruction)
    RTL



Unlocks:
    LDA $F02018             ; load party member unlocks from SRAM
    STA $0780               ; transfer to flags (WRAM)
    LDA $F02019             ; load capsule monster unlocks from SRAM
    TAY
    LDX.w #$0000
-:  TYA
    LSR
    TAY
    BCC +
    LDA $82C33C
    CMP $11BB,X
    BMI +++
    BRA ++
+:  LDA.b #$00
++: STA $11BB,X             ; unlock/lock capsule monster #X
+++ INX
    CPX.w #$0007
    BNE -
    LDA $F02019
    TAY
    BNE +
    LDA.b #$FF
    STA $0A7F               ; lock capsule menu
    BRA ++
+:  LDA.b #$07
    STA $0A7F               ; unlock capsule menu
    LDA $F02019
    BIT.b #$80              ; track whether one-time setup has been done before
    BNE ++
    ORA.b #$80
    STA $F02019
    CMP.b #$FF
    BEQ ++                  ; all capsule monsters available; don't overwrite starting capsule
    LDX.w #$FFFF
    TYA
-:  LSR
    INX
    BCC -
    TXA
    STA $11A3               ; activate first unlocked capsule monster
    STA $7FB5FB
    STA $F02016
    JSL $82C2FD             ; run setup routine for capsule monsters
++: RTS



; lock party members
pushpc
org $8AEC3E
    DB $15,$C4,$A4,$01      ; L2SASM JMP $8AEB1C+$01A4 if flag $C4 set
org $8AECC0
    DB $6C,$65,$00,$FA          ; (overwritten instruction)
    DB $15,$12,$AE,$01,$2E,$66  ; remove selan if flag $12 clear
    DB $15,$13,$B4,$01,$2E,$67  ; remove guy if flag $13 clear
    DB $15,$14,$BA,$01,$2E,$68  ; remove arty if flag $14 clear
    DB $15,$15,$C0,$01,$2E,$6A  ; remove dekar if flag $15 clear
    DB $15,$16,$C6,$01,$2E,$69  ; remove tia if flag $16 clear
    DB $15,$17,$CC,$01,$2E,$6B  ; remove lexis if flag $17 clear
    DB $00
pullpc



; party member items (IDs $01B2 - $01B7)
pushpc
org $96F875  ; properties
    DB $40,$00,$00,$E9,$64,$00,$00,$00,$00,$00,$00,$00,$00
    DB $40,$00,$00,$E0,$64,$00,$00,$00,$00,$00,$00,$00,$00
    DB $40,$00,$00,$EB,$64,$00,$00,$00,$00,$00,$00,$00,$00
    DB $40,$00,$00,$ED,$64,$00,$00,$00,$00,$00,$00,$00,$00
    DB $40,$00,$00,$E8,$64,$00,$00,$00,$00,$00,$00,$00,$00
    DB $40,$00,$00,$EF,$64,$00,$00,$00,$00,$00,$00,$00,$00
org $979EC6  ; descriptions
    DB "Parcelyte commander.    "    : DB $00
    DB "A guy named Guy.  "          : DB $00
    DB "(Or was it Artea?)         " : DB $00
    DB "Strongest warrior.   "       : DB $00
    DB "Elcid shopkeeper. "          : DB $00
    DB "Great inventor."             : DB $00
org $97FDAC  ; remove from scenario item list
    DW $0000,$0000,$0000,$0000,$0000,$0000
org $9EDC40  ; names
    DB "Selan       "       ; overwrites "Wind key    "
    DB "Guy         "       ; overwrites "Cloud key   "
    DB "Arty        "       ; overwrites "Light key   "
    DB "Dekar       "       ; overwrites "Sword key   "
    DB "Tia         "       ; overwrites "Tree key    "
    DB "Lexis       "       ; overwrites "Flower key  "
pullpc

; capsule monster items (IDs $01B8 - $01BE)
pushpc
org $96F8C3  ; properties
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
    DB $00,$00,$00,$EE,$12,$00,$00,$00,$00,$00,$00,$00,$00
org $979F47  ; descriptions
    DB "NEUTRAL        "                : DB $00
    DB "LIGHT             "             : DB $00
    DB "WIND           "                : DB $00
    DB "WATER                         " : DB $00
    DB "DARK                      "     : DB $00
    DB "SOIL                       "    : DB $00
    DB "FIRE                       "    : DB $00
org $9EDC88  ; names
    DB "JELZE       "       ; overwrites "Magma key   "
    DB "FLASH       "       ; overwrites "Heart key   "
    DB "GUSTO       "       ; overwrites "Ghost key   "
    DB "ZEPPY       "       ; overwrites "Trial key   "
    DB "DARBI       "       ; overwrites "Dankirk key "
    DB "SULLY       "       ; overwrites "Basement key"
    DB "BLAZE       "       ; overwrites "Narcysus key"
pullpc



; receive death link
pushpc
org $83BC91
    ; DB=$83, x=0, m=1
    JSL DeathLinkRX         ; overwrites LDA $7FD0AE
pullpc

DeathLinkRX:
    LDA $F0203F             ; check death link trigger
    BEQ +
    TDC
    STA $F0203F             ; reset death link trigger
    LDA $F0203D             ; check death link enabled
    BEQ +
    LDA.b #$04
    STA $0BBC               ; kill maxim
    STA $0C7A               ; kill selan
    STA $0D38               ; kill guy
    STA $0DF6               ; kill arty
    STA $0EB4               ; kill tia
    STA $0F72               ; kill dekar
    STA $1030               ; kill lexis
    LDA.b #$FE
    STA $7FF8A3             ; select normal enemy battle
    LDA.b #$82
    STA $7FF8A4             ; select a formation containing only demise
    JSL $8383EB             ; force battle
+:  LDA $7FD0AE             ; (overwritten instruction)
    RTL

DeathLinkTX:
    LDA $F0203D             ; check death link enabled
    BEQ +
    LDA $7FF8A4             ; load formation number
    CMP.b #$82              ; did we die from a death link?
    BEQ +
    STA $004202
    LDA.b #$0A
    STA $004203             ; multiply by 10 to get formation offset
    TDC
    NOP
    LDA $004216
    TAX
    LDA $7FF756,X           ; read first monster in formation
    INC
    STA $F0203E             ; send death link by monster id + 1
+:  RTL



; clear receiving counters when starting new game; force "GIFT" mode
pushpc
org $83AD83
    ; DB=$83, x=0, m=1
    JSL ClearRX             ; overwrites BIT #$02 : BEQ $83ADAB
pullpc

ClearRX:
    REP #$20
    TDC
    STA $F02800             ; clear received count
    STA $F02802             ; clear processed count
    SEP #$20
    ; absence of the overwritten instructions automatically leads to "GIFT" mode code path
    RTL



; store receiving counters when saving game
pushpc
org $82EB61
    ; DB=$8A, x=0, m=1
    JSL SaveRX              ; overwrites JSL $8090C9
pullpc

SaveRX:
    JSL $8090C9             ; (overwritten instruction) write save slot A to SRAM
    SEP #$10
    REP #$20
    ASL
    ASL
    TAX
    LDA $F02800             ;
    STA $F027E0,X           ; save received count
    LDA $F02802             ;
    STA $F027E2,X           ; save processed count
    SEP #$20
    REP #$10
    RTL



; restore receiving counters when loading game
pushpc
org $82EAD5
    ; DB=$83, x=0, m=1
    JSL LoadRX              ; overwrites JSL $809099
pullpc

LoadRX:
    JSL $809099             ; (overwritten instruction) load save slot A from SRAM
    SEP #$10
    REP #$20
    ASL
    ASL
    TAX
    LDA $F027E0,X           ;
    STA $F02800             ; restore received count
    LDA $F027E2,X           ;
    STA $F02802             ; restore processed count
    SEP #$20
    REP #$10
    RTL



; keep inventory after defeat
pushpc
org $848B9C
    ; DB=$7E, x=0, m=1
    NOP #5                  ; overwrites LDA.b #$FF : STA $7FE759 : JSR $8888
    JSL DeathLinkTX
pullpc



; set initial floor number
pushpc
org $8487A9
    JSL InitialFloor        ; overwrites TDC : STA $7FE696
    NOP
pullpc

InitialFloor:
    LDA $D08015             ; read initial floor number
    STA $7FE696             ; (overwritten instruction)
    TDC                     ; (overwritten instruction)
    RTL



; report final floor goal completion
pushpc
org $839E87
    JSL FinalFloor          ; overwrites STA $0005B0
pullpc

FinalFloor:
    STA $0005B0             ; (overwritten instruction)
    LDA.b #$01
    STA $F02034             ; report final floor goal
    RTL



; start with Providence
pushpc
org $8488BB
    ; DB=$84, x=0, m=0
    SEC                     ; {carry clear = disable this feature, carry set = enable this feature}
    JSL Providence          ; overwrites LDX.w #$1402 : STX $0A8D
    NOP                     ;
pullpc

Providence:
    LDX.w #$1402            ; (overwritten instruction)
    STX $0A8D               ; (overwritten instruction) add Potion x10
    BCC +
    LDX.w #$022D            ;
    STX $0A8F               ; add Providence
+:  RTL



; start inventory
pushpc
org $848901
    ; DB=$84, x=0, m=1
    JSL StartInventory      ; overwrites JSL $81ED35
pullpc

StartInventory:
    JSL $81ED35             ; (overwritten instruction)
    REP #$20
    LDA $F02802             ; number of items to process
    DEC
    BMI ++                  ; skip if empty
    ASL
    TAX
-:  LDA $F02804,X           ; item ID
    BPL +                   ; spells have high bit set
    PHX
    JSR LearnSpell
    PLX
+:  BIT.w #$C000            ; ignore blue chest items (and spells)
    BNE +
    PHX
    STA $09CF               ; specify item ID
    TDC
    INC
    STA $09CD               ; specify quantity as 1
    JSL $82E80C             ; add item to inventory
    REP #$20
    PLX
+:  DEX
    DEX
    BPL -
++: SEP #$20
    RTL



; increase variety of red chest gear after B9
pushpc
org $839176
    ; DB=$7F, x=0, m=1
    CLC                     ; {carry clear = disable this feature, carry set = enable this feature}
    JSL RedChestGear        ; overwrites LDX.w #$1000 : LDA $60
org $83917D
    ; DB=$7F, x=0, m=1
    JSL RunEquipmentRNG     ; overwrites LSR : JSR $9E11
pullpc

RedChestGear:
    BCC +
    REP #$20                ; support more than 127 items
+:  LDX.w #$1000            ; (overwritten instruction)
    LDA $60                 ; (overwritten instruction)
    RTL
RunEquipmentRNG:
    BCS +
    SEP #$20
    PHK
    PEA ++
    PEA $8DD8
    LSR
    JML $839E11
+:  LSR                     ; (overwritten instruction) divide by 2 (translates max item offset to max item number)
    SEP #$20                ; (the max item number fits in 8bits since there are always fewer than 256 eligible items)
    STA $004202             ; run RNG: fill WRMPYA multiplicand register with max item number
    JSL $8082C7             ; run RNG: load 8bit accumulator with 1st random number from PRNG
    STA $004203             ; run RNG: fill WRMPYB multiplier register with 1st random number and start multiplication
    NOP
    REP #$20
    LDA $004216             ; run RNG: read RDMPYL+H multiplication result
    STA $E746,Y             ; save it for later
    SEP #$20
    JSL $8082C7             ; run RNG: load 8bit accumulator with 2nd random number from PRNG
    STA $004203             ; run RNG: fill WRMPYB multiplier register with 2nd random number and start multiplication
    CLC
    TDC
    LDA $004217             ; run RNG: read RDMPYH multiplication result
    REP #$20
    ADC $E746,Y
    AND.w #$FF00
    XBA
    ASL                     ; multiply by 2 (translates selected item number to selected item offset)
++: TAX                     ; store result in 16bit X register
    RTL



; relocate capsule cravings table
pushpc
org $82C55A
    LDA $D09200,X           ; overwrites LDA $95FF16,X
org $82C55F
    LDA $D09202,X           ; overwrites LDA $95FF18,X
org $82C572
    LDA $D09200,X           ; overwrites LDA $95FF16,X
pullpc



; set capsule monster starting xp
pushpc
org $82C313
    ; DB=$84, x=0, m=1
    JSL CapsuleStartingXp   ; overwrites LDX.w #$0000 : LDA.b #$00 : STA $7FF1AA,X : INX : CPX.w #$0015 : BNE $82C318
    NOP #11
pullpc

CapsuleStartingXp:
    PHB
    REP #$20
    LDA $D08012
    STA $7FF1AA             ; store low word of starting XP for first capsule monster
    SEP #$20
    LDA $D08014
    STA $7FF1AC             ; store highest byte of starting XP for first capsule monster
    TDC
    LDA.b #$11
    LDX.w #$F1AA
    LDY.w #$F1AD
    MVN $7F,$7F             ; pattern fill the remaining six capsule monster slots
    PLB
    RTL



; set starting capsule monster
pushpc
org $82C36A
    ; DB=$83, x=0, m=1
    JSL StartingCapsule     ; overwrites STZ $11A3 : LDA.b #$01
    NOP
pullpc

StartingCapsule:
    LDA $F02016             ; read starting capsule monster id
    STA $11A3
    LDA.b #$01              ; (overwritten instruction)
    RTL



; enter ancient cave as if coming from the world map
pushpc
org $83B773
    ; DB=$7E, x=0, m=1
    JSL CaveEntrance        ; overwrites LDA $05AC : STA $05B4
    NOP #2
pullpc

CaveEntrance:
    LDA $05AC               ; (overwritten instruction)
    CMP.b #$68
    BNE +                   ; when leaving gruberik, act as if leaving world map
    TDC
+:  STA $05B4               ; (overwritten instruction)
    RTL



; enable run button
; directional input item crash fix
pushpc
org $83FC6C
    REP #$10                ; overwrites BEQ $83FC8A : LDA.b #$80
    LDA.b #$40
pullpc



; mid-turn death fix
pushpc
org $85B544
    JSL MidTurnDeathFix     ; overwrites JSL $85CCCE
pullpc

MidTurnDeathFix:
    JSL $85CCCE             ; (overwritten instruction) clear shared battle registers after attack
    LDY.w #$000F            ; offset to status effect byte
    LDA ($BE),Y             ; offset to stat block of attacker
    BIT.b #$04              ; check death
    BEQ +
    TSX                     ; attacker died; abort script
    INX #3
    TXS
    JML $85B476
+:  RTL                     ; attacker still alive; continue script



; poison death fix
pushpc
org $818959
    JSL PoisonDeathFix      ; overwrites JSL $859DD4
pullpc

PoisonDeathFix:
    JSL $859DD4             ; (overwritten instruction)
    JSL $8593B7
    RTL



; single-node room fix
pushpc
org $839C64
    ; DB=$7F, x=0, m=1
    BNE +                   ; overwrites BNE $17
org $839C7B
    ; DB=$7F, x=0, m=1
    JMP $9BE7               ; overwrites BRA $22 : LDX.w #$00FF
+:  TDC
    TAX
org $839C99
    ; DB=$7F, x=0, m=1
    INX                     ; overwrites DEX : CPX.w #$0010 : BCS $E1
    CPX.w #$0100
    BCC $E1
pullpc



; equipment text fix
pushpc
org $81F2E3
    ; DB=$9E, x=0, m=1
    NOP #2                  ; overwrites BPL $81F2D6
pullpc



; music menu fix
pushpc
org $82BF44
    ; DB=$83, x=0, m=1
    BNE $12                 ; overwrites BNE $06
pullpc



; logo skip
pushpc
org $80929A
    ; DB=$80, x=0, m=1
    LDA.b #$00              ; overwrites LDA.b #$80
pullpc



; intro skip
pushpc
org $8080CF
    ; DB=$80, x=1, m=1
    JML $8383BD             ; overwrites JML $808281
pullpc



; SRAM map
; $F02000   16  signature
; $F02010   2   blue chest count
; $F02012   3   capsule starting xp
; $F02015   1   initial floor
; $F02016   1   starting capsule
; $F02017   1   iris treasures required
; $F02018   1   party members available
; $F02019   1   capsule monsters available
; $F02030   1   selected goal
; $F02031   1   goal completion: boss
; $F02032   1   goal completion: iris_treasure_hunt
; $F02033   1   goal completion: master_iris_treasure_hunt
; $F02034   1   goal completion: final_floor
; $F0203D   1   death link enabled
; $F0203E   1   death link sent (monster id + 1)
; $F0203F   1   death link received
; $F02040   2   check counter (snes_items_sent)
; $F02042   2   check counter (client_items_sent)
; $F02044   2   check counter (client_ap_items_found)
; $F02046   2   check counter (snes_ap_items_found)
; $F027E0   16  saved RX counters
; $F02800   2   received counter
; $F02802   2   processed counter
; $F02804   inf list of received items
