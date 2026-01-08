hirom
; custom item hacking

org $C2BB02
JML CustomItem

org $C2BCB1
JML AllowItemWarping


org !ADDRESS_customitem1
CustomItem:

if !fourjobmode == 1
    if !fourjoblock == 1
        ; Load in A
        LDA $7A00,X

        cmp #$EE ; warpshard
        beq CustomItemTestFourJob
        ; cmp #$3E ; Exit spell
        ; beq CustomItemTestFourJob
        cmp #$F0 ; tent
        beq CustomItemTestFourJob
        cmp #$F1 ; cabin
        beq CustomItemTestFourJob
        bne ContinueCustomItemStart1

        CustomItemTestFourJob:
        JSL FourJobSubroutineCheck
        CMP #$01 ; success case
        BEQ ContinueCustomItemStart1
        ; failure case 
        JMP ProceedRejectedItemFinish
        
        ContinueCustomItemStart1:
        ; proceed as usual if conditions are met
    endif 
endif 


; Load in A 
LDA $7A00,X
; If specific conditions met, do something else


; Using $EE for custom item 1
CMP #$EE
BEQ CustomItemEvent1
; CMP #$3E
; BEQ CustomItemEvent1
; if no condition met
BNE ProceedRegularItem

ProceedRegularItem:
JMP ProceedRegularItemFinish


; Custom item - attempting an event
CustomItemEvent1:
; ALL CONDITIONALS FOR MAP BLOCKING HAPPENS HERE. 
; IF ANY CONDITION FAILS, the item id "F8" is loaded, which is OmegaMedl - all it means is that it will return a non-action upon trying to use the item (and a nice little sound effect). 
; 000AD5 000AD6 are map locations. the below references are in LE format

rep #$20
lda $0AD5
; sealed room of kuzar
CMP #$3601
BEQ ProceedRejectedItem
; sealed room of kuzar
CMP #$4201
BEQ ProceedRejectedItem
; Pirate cave entrance
CMP #$1200
BEQ ProceedRejectedItem
; Wind shrine chamber
CMP #$1F00
BEQ ProceedRejectedItem
; Torna Canal
CMP #$2800
BEQ ProceedRejectedItem
; Karnak castle
CMP #$5700
BEQ ProceedRejectedItem
; Water shrine chamber
CMP #$7300
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8300
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8400
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8500
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8600
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8700
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8800
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8900
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8A00
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8B00
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8C00
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8D00
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8E00
BEQ ProceedRejectedItem
; Karnak castle
CMP #$8F00
BEQ ProceedRejectedItem
; Karnak castle
CMP #$9000
BEQ ProceedRejectedItem
; Karnak castle
CMP #$9100
BEQ ProceedRejectedItem
; Karnak castle
CMP #$9200
BEQ ProceedRejectedItem
; Airship
CMP #$BE00
BEQ ProceedRejectedItem
BNE CustomItemEvent1Checking2

ProceedRejectedItem:
JMP ProceedRejectedItemFinish

CustomItemEvent1Checking2:
; Bchoco
CMP #$BF00
BEQ ProceedRejectedItem2
; Fire powered ship boiler room
CMP #$A200
BEQ ProceedRejectedItem2
; Earth crystal chamber
CMP #$DC00
BEQ ProceedRejectedItem2
; Zeza fleet
CMP #$4601
BEQ ProceedRejectedItem2
; Zeza fleet below deck
CMP #$4701
BEQ ProceedRejectedItem2
; ; Submarine
; CMP #$5701
; BEQ ProceedRejectedItem2
; Death Valley
CMP #$7201
BEQ ProceedRejectedItem2
; Antlion's nest
CMP #$7301
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8901
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8A01
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8B01
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8C01
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8D01
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8E01
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$8F01
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9001
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9101
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9201
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9301
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9401
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9501
BEQ ProceedRejectedItem2
; Fork Tower
CMP #$9601
BEQ ProceedRejectedItem2
BNE CustomItemEvent1Checking3

ProceedRejectedItem2:
JMP ProceedRejectedItemFinish

CustomItemEvent1Checking3:

; Mua Forest transformation
CMP #$6B01
BEQ ProceedRejectedItem3
; Mua Forest transformation
CMP #$6601
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9701
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9801
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9901
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9A01
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9B01
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9C01
BEQ ProceedRejectedItem3
; Fork Tower
CMP #$9D01
BEQ ProceedRejectedItem3
; Magic Lamp
CMP #$1F01
BEQ ProceedRejectedItem3
; Ronka outside sol cannon
CMP #$DD00
BEQ ProceedRejectedItem3
; Ronka outside sol cannon
CMP #$D200
BEQ ProceedRejectedItem3

BNE CustomItemEvent1Pass

ProceedRejectedItem3:
JMP ProceedRejectedItemFinish


CustomItemEvent1Pass:
sep #$20
LDA #$B1
STA $C7
LDA #$BC
STA $C8
LDA #$EE ; <<<<<<<<<<<< This is setting the conditional for checking if "WARP" got called. F0 = tent, F1 = cabin, 3E = warp. Corresponds to EVENTS
STA $39
JML $C2A335

JMP FinishCustomItem


FinishCustomItem:
; Original code and branch
; PHX
JML $c2bbac

ProceedRegularItemFinish:
; reload in A
LDA $7A00,X
; Original code and branch
STA $29E7
PHX
JML $C2BB09

ProceedRejectedItemFinish:
sep #$20
; Load in specifically omegamedl for failed item use
LDA #$F8

; play sound
LDA #$6E ; <<<< Change this for the sound effect. Refer to event_data.py in the Event Parser subdir
STA $1D01
LDA #$02
STA $1D00
LDA #$0F
STA $1D02
LDA #$88
STA $1D03
JSL $C40004


; Original code and branch
STA $29E7
PHX
JML $C2BB09



org $C0011F
JML UseableItemActionTable

org !ADDRESS_customitem2
UseableItemActionTable:
LDA $0139
; This is for any custom action table from above. You can use any code you'd like as long as its not F0, F1 or 3E
; This would be corresponding to similar events like CustomItemEvent1 above 
CMP #$EE
BEQ UseableItemEE
; EDIT - Commented the below, was old code for the Exit spell. 
; CMP #$3E ; do the same for Exit spell. 
; BEQ UseableItemEE
BNE PreReturnToItemChecking
UseableItemEE:
LDX #$003A ; Removes unused pyramid cutscene from w3 where party discovers quicksand stopped
JML $C0013B ; now with x loaded, go back to event


PreReturnToItemChecking:
; Perform enough of old code and jump back:
CMP #$F0
BEQ JumpToItemF0
BNE ReturnToItemChecking

JumpToItemF0:
JML $C00126

ReturnToItemChecking:
JML $C0012B


AllowItemWarping:




STA $39


; TO DO
; You hooked in here (the magic warp event switcher), which is perhaps too late into the chain
; for denying magic from being cast
; Try hooking into the magic menu earlier when the game
; is validating stuff like Time Mage ability, sufficient magic
; then reject there if four job conditions aren't met 
 
if !fourjobmode == 1
    if !fourjoblock == 1
        CMP #$3E
        BNE ContinueExitSpellFourJob
        ; if it is exit spell, do the check
        JSL FourJobSubroutineCheck
        CMP #$01 ; success case
        BEQ ContinueAllowItemWarping1
        ; failure case defaults 
        BNE BranchToItemWarpClause2
        
        ContinueExitSpellFourJob:
    endif 
endif

CMP #$EE ; custom item1 
BEQ BranchToItemWarpClause
; CMP #$3E ; Exit spell
; BEQ BranchToItemWarpClause
ContinueAllowItemWarping1:
LDA $44
AND #$02
BEQ BranchToItemWarpClause2
BNE BranchToItemWarpClause

BranchToItemWarpClause2:
JML $C2BCA9

BranchToItemWarpClause:
PHA
LDA #$00
STA $7E29E8
STA $7E29E9
PLA
JML $C2BCB9


; ; CUSTOM CODE TO ALLOW SHOAT SOUND EFFECT WITHOUT AWARDING
; org $c2bb66
; JML !ADDRESS_shoatsound

; org !ADDRESS_shoatsound
; ; if using EE item (WarpShard), don't award player anything
; sep #$20
; PHA
; LDA $7A00,X
; CMP #$EE
; BEQ SkipSummonAward


; ; Else, do the reward, then branch back
; PLA
; rep #$20
; AND #$00FF
; SEC
; SBC #$00F8
; TAX
; LDA $C0EEAE,X
; JML $C2BB72

; ; SkipSummonAward:
; ; just branch back
; ; PLA
; ; JML $C2BB72

; Data rewrites:
; Allow for item $EE to be used 
; org $C0EEF2
; db $EE

; Remove item $12 for now to end loop code...?
;org $C0EEF4
;db $00

; WarpShard cannot sell
org $D12BDC
db $81, $00

; WarpShard will have an item description now
org $D10AF3
db $A7
; ... and OmegaMedal/DragonCrest will not
org $D10B3B
db $80
org $D10B43
db $80

; Overwrite OmegaMedal/DragonCrest text
org $D144D0
db $76, $7A, $8B, $89, $96, $7B, $7E, $8D, $90, $7E, $7E, $87, $96, $90, $88, $8B, $85, $7D, $8C, $96, $96,$96,$96,$96,$96,$96,$96,$96, $74, $8C, $7E, $7A, $7B, $85, $7E, $96, $82, $87, $96, $86, $88, $8C, $8D, $96, $85, $88, $7C, $7A, $8D, $82, $88, $87, $8C, $00 

; change references to custom table for useable items/magic
org $c2dadc
LDA !ADDRESS_useableitemstable, X
org $c2e413
LDA !ADDRESS_useableitemstable, X

; recreate custom table for useable items
org !ADDRESS_useableitemstable
db $e0, $13, $e1, $13, $e2, $13, $e3, $13, $e4, $13, $e5, $13, $e6, $13, $e8, $13, $e9, $13, $ec, $13, $ed, $13, $f0, $00, $f1, $00, $f9, $44, $fa, $47, $fb, $4b
;   NEW ITEM
db $EE, $00
;   END
db $00, $00

