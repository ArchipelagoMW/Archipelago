hirom

org $C0CAB2
; Step counter increaser area 
; These are the step increasers
JML EncounterHook
nop
nop
nop
nop

org !ADDRESS_encounterhook
EncounterHook:
sep #$20

LDA !encounterswitch
AND #$80
BPL EncountersOn

; Code executes if encounters are off
rep #$20
LDA #$0000
CLC
BEQ Finish2

; standard code for when encounters are on 
EncountersOn:
rep #$20
if !everysteprandomencounter = 1
    LDA #$FFFF
else
    LDA $16A8
endif
BEQ Finish


Finish:
CLC
ADC $c0cb09,x

Finish2:

JML $C0CABA








; Hook for world map encounters
; These are the step increasers
org $c0cbbe
JML WorldMapHook

org !ADDRESS_worldmaphook
WorldMapHook:

sep #$20

; swap speed if input == B:
JSL SpeedHookGeneric
STA !speedvalue

LDA !encounterswitch
AND #$80
BPL WorldMapReturnEnc


rep #$20
lda #$0000
sta $16a8
lda $06
sep #$20
JML $c0cbc5

WorldMapReturnEnc:
rep #$20
if !everysteprandomencounter = 1
    LDA #$FFFF
endif
sta $16a8
lda $06
sep #$20
JML $c0cbc5


















; ; Frame by frame hook, NOT in menu

; org ###$C0043F
; nop
; nop

; JML FrameHook

; org $
; FrameHook:


; PHA


; ; do stuff 



; PLA ; pull A from above


; ; original instructions
; PLD
; PLB
; PLY
; PLX
; PLA
; PLP
; JML $C00445








; menu fix for resetting shop hook for $C0 value
; this allows summon items to properly award

; 0001C7 has the subroutine jumper  

org $c2a033
JML !ADDRESS_menusummonsfix

org !ADDRESS_menusummonsfix

lda #$00
sta $7E2802

; original code
lda $35
sta $44 
lda #$01
JML $c2a039







; For MENU frame by frame
org $C2FBE9
JML FrameHookMenu

org !ADDRESS_menuhook

FrameHookMenu:
PHA
PHX
PHY

; this code will block out the 4/5/6 on the config menu
; due to the index system and ROM data, the game automatically copies the "1 2 3 4 5 6 " twice from ROM, so it's not possible to isolate "1 2 3" for walk speed
; therefore, we use vram to block it out, which is only active in the config menu 


sep #$20
lda !configmenucheck ; load config menu id
CMP #$06 ; if anything else, branch 
bne FinishFrameHookMenu ;old CheckDestinationWriter
lda !configmenucheck2 ; load config menu id
CMP #$f6 ; if anything else, branch 
bne FinishFrameHookMenu ;old CheckDestinationWriter

; this writes to vram 

LDA #$53  ; WRITE address  - location of "3" , but change it to FOUR
STA $002116
LDA #$11  ; WRITE address
STA $002117
LDA #$80
STA $002115

LDA #$57
STA $002118



LDA #$55  ; WRITE address  - location of "4" 
STA $002116
LDA #$11  ; WRITE address
STA $002117
LDA #$80
STA $002115

LDA #$96
STA $002118



LDA #$57  ; WRITE address  - location of "5" 
STA $002116
LDA #$11  ; WRITE address
STA $002117
LDA #$80
STA $002115

LDA #$96
STA $002118

LDA #$59  ; WRITE address  - location of "6" 
STA $002116
LDA #$11  ; WRITE address
STA $002117
LDA #$80
STA $002115

LDA #$96
STA $002118

lda #$00
sta $7E5000
rep #$20
JML FinishFrameHookMenu


; this code will check for destinations
; it confirms if in the item menu $7E0143 == $07
; then confirms if the pointer is on the Rare icon $7E0200 == $A8
; then confirms if the "Rare" menu is actually selected $7E01E0 == $00, then triggers text
; if all conditions met, then write destination data and trigger via storing $01 in $7E7511

; still in 8 bit mode
; CheckDestinationWriter:
; lda !menutype
; CMP #$07
; BNE FinishFrameHookMenuHook
; lda !itemmenuloc 
; CMP #$A8
; BNE FinishFrameHookMenuHook
; lda !itemmenuvalidater
; CMP #$00
; BNE ClearItemText ; here, if leaving the "Rare" menu, set back to no text
; BEQ FillItemText

; FinishFrameHookMenuHook:
; JML FinishFrameHookMenu
; ; if conditions met, then execute destination writer
; ; !destinationdata2 - lookup table for index 
; ; Load in value at $7EF87F and asl 5 times to get an index location
; ; Example base F18300 (UPDATE: old code, changed to $E7 bank instead of $F1)
; ; Value at $7EF87F is 02
; ; $0002 asl x5 → $0020
; ; then index will be $F18500

; ; 28 characters per per line
; FillItemText:
; ldx #$0000 ; First loop for "Destination"
; ldy #$0000 ; First loop for "Destination"
; FillTextLoop1st:
    ; lda !destinationdata1, x ; begins at index, increases x until 28 char limit
    ; sta $51C4, y
    ; inx
    ; iny
    ; iny
    ; CPY #$0038 ; Max chars in hex
    ; BNE FillTextLoop1st

; rep #$20
; lda #$0000
; sep #$20
; lda !destinationindex
; rep #$20
; asl
; asl
; asl
; asl
; asl  ; now an index 
; TAX
; sep #$20

; ldy #$0000 ; 28 character limit to length of line 
; FillTextLoop:
    ; lda !destinationdata2, x ; begins at index, increases x until 28 char limit
    ; sta $5244, y
    ; inx
    ; iny
    ; iny
    ; CPY #$0038 ; Max chars in hex
    ; BNE FillTextLoop

; lda #$01
; sta !itemboxwriter
; JML FinishFrameHookMenu

; ClearItemText:
; LDA #$FF
; LDX #$0000
; ClearTextLoop1st:
    ; sta $51C4, x
    ; inx
    ; inx
    ; CPX #$0038 ; Max chars in hex
    ; BNE ClearTextLoop1st
; LDX #$0000    
; ClearTextLoop:
    ; sta $5244, x
    ; inx
    ; inx
    ; CPX #$0038 ; Max chars in hex
    ; BNE ClearTextLoop

; lda #$01
; sta !itemboxwriter
; JML FinishFrameHookMenu







FinishFrameHookMenu:
; original instructions
rep #$20
PLY
PLX
PLA

LDA #$0001
clc
ADC $094a
STA $094a

JML $C2FBF3



org $C0106E
JML AirshipSlowDownHook

org !ADDRESS_airshipslowdown
AirshipSlowDownHook:
pha
lda !input2
cmp #$80
bpl AirshipSlowDownApplySlowDown
bmi AirshipSlowDownApplyNormal

AirshipSlowDownApplySlowDown:
LDA $0ADC
CMP #$06 ; 06 = airship 
BEQ AirshipSlowDownApplySlowDownAirship
BNE AirshipSlowDownApplySlowDownNotAirship
AirshipSlowDownApplySlowDownAirship:
LDA #$04
STA !speedvalue
JMP AirshipSlowDownFinish
AirshipSlowDownApplySlowDownNotAirship:
LDA #$02
STA !speedvalue
JMP AirshipSlowDownFinish


AirshipSlowDownApplyNormal:
LDA $0ADC
CMP #$06 ; 06 = airship 
BEQ AirshipSlowDownApplyNormalAirship
BNE AirshipSlowDownApplyNormalNotAirship
AirshipSlowDownApplyNormalAirship:
; now quickly check if boat or not
LDA $0AF1
AND #$0F
CMP #$05
BEQ AirshipSlowDownApplyNormalNotAirship ; if $55, ignore
; now check if in world 3 underwater and adjust accordingly
LDA $0AD4
CMP #$04
BNE AirshipSlowDownApplyNormalNotAirship1
LDA #$08
STA !speedvalue
JMP AirshipSlowDownApplyNormalNotAirshipFinish
AirshipSlowDownApplyNormalNotAirship1:
LDA #$20
STA !speedvalue
AirshipSlowDownApplyNormalNotAirshipFinish:
JMP AirshipSlowDownFinish
AirshipSlowDownApplyNormalNotAirship:
LDA #$08
STA !speedvalue
JMP AirshipSlowDownFinish

; original code and return
AirshipSlowDownFinish:
pla
dec
asl a
asl a
tay
lda $0add,y
JML $C01075
