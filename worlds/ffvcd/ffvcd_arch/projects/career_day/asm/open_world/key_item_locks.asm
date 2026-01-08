hirom


; RIFT CASTLE DOOR
; flag 0A42 bit 04 is tied to catastrophe
; flag 0A42 bit 20 is tied to halicarnassus
org $F06009
db $FC, $75, $f7, $00, $fb, $03, $f6, $ff, $a2, $06



; STEAMSHIP LOCK

; new code area for conditional checking. EACH X/Y CHECKER HAS A CORRESPONDING OUTPUT HERE
; org $D8FFA8
org $F05F28
!keyitemarea = $FC, $B6

; Simple example, does not allow for directional confirm for something like a door
; db !keyitemarea, $FF, $4C, $00, $FF, $F0, $00

; Complex example, checks each direction first and nulls event, but if it's the matching direction, proceed with conditionals for checking key item flag then running event 
db $F7, $01, $FF, $00, $00, $F7, $02, $FF, $00, $00, $F7, $03, $FF, $00, $00, $F7, $00, !keyitemarea, $FF, $4C, $00, $FF, $F0, $00




; BIG BRIDGE
; first find area where it reads how many bytes to check for the map
org $CE2678
; redefine byte in this specific area to be 2 more from the outside area
db $88, $0D
; 2) how many bytes to check by defining last address to read in
; db $68, $12


; what x/y to check, then 2 bytes of action if so
; original for BIG BRIDGE is CE3190, moved to below:
org $CE3188
; new stuff.  YOU DON'T HAVE TO CARE ABOUT THE 3RD/4TH ARGUMENT HERE, BECAUSE YOU MANUALLY TREAT LATER
; write doorway to overwrite other cutscene, here at $F0 $00
db $2F, $12, $00, $00
; write doorway to overwrite other cutscene, here at $F1 $00
db $0D, $0B, $00, $00


; new code area for conditional checking
; second argument is LOCK_ID from "Key Items" sheet
; org $D8FFC2
org $F05F42
!keyitemarea = $FC, $B3

; No direction required here, just step on tile
; Failure case, blocking textbox & step down
; In this case, no need for another event on sucess case, just allow access, because door panel works fine
db !keyitemarea, $FF, $00, $00, $FF, $4D, $00
db !keyitemarea, $FF, $00, $00, $FF, $59, $00




; SUBMARINE BARRIER TOWER ACCESS

; org $D8FFD2
org $F05F52

; No direction required here, just step on tile
; Failure case, blocking textbox & step down
; In this case, no need for another event on sucess case, just allow access, because door panel works fine
db $FF, $F8, $00




; SOLITARY SHRINE PAGE 
; org $D8FFD6
org $F05F56
db $FB, $BB, $FF, $F4, $00, $FB, $66, $FF, $93, $06, $FF, $00, $00
; TRENCH PAGE 
;org $D8FFE3
org $F05F63
db $FB, $BA, $FF, $F4, $00, $FD, $A1, $FF, $C2, $05, $FF, $00, $00
; FALLS PAGE 
;org $D8FFF0
org $F05F70
db $FB, $B9, $FF, $F4, $00, $FB, $76, $FF, $94, $06, $FF, $00, $00


; RIFT TABLET CHECKING
; org $D90000
org $F05F80
db $F7, $02, $FF, $00, $00, $FB, $69, $FF, $FF, $00, $FB, $68, $FF, $05, $01, $FF, $07, $01


; TORNA CANAL
;org $D90015
org $F05F95
db $FC, $22, $ff, $9e, $00, $FB, $22, $ff, $77, $00


; SHOAT CAVE
org $F05FA0
db $F7, $02, $FF, $00, $00, $FE, $C0, $ff, $BD, $01, $FE, $C1, $ff, $BD, $01, $FE, $C2, $ff, $BD, $01, $FE, $C3, $ff, $BD, $01, $FE, $C4, $ff, $BD, $01, $FE, $C5, $ff, $BD, $01, $FE, $C7, $ff, $BD, $01, $ff, $BE, $01

; PHOENIX TOWER
;org $D90015
org $F05FCB
db $FE, $5A, $FF, $00, $00, $FD, $65, $FF, $43, $00, $FE, $F63, $FF, $27, $00, $FD, $F63, $FF, $22, $00

; PORTAL BOSS
org $F05FDF
    ; bit A49 $01 = boss fight was triggered
        ; Corresponds to conditional set FC A8 and event code A4 A8 
    ; bit A49 $02 = boss fight was ended properly with dialogue final form
        ; Corresponds to conditional set FC A9 and event code A4 A9 
        
    ; if any tablets aren't acquired, reject
    db $FB, $CA, $FF, $A3, $05
    db $FB, $CB, $FF, $A3, $05
    db $FB, $CC, $FF, $A3, $05
    db $FB, $CD, $FF, $A3, $05
    
    
    ; If boss triggered and fight ended properly
    db $FC, $A8, $FC, $A9, $FF, $A7, $05 ; <<<<<< CHANGE THIS EVENT
    ; If boss triggered and fight NOT ended properly
    db $FC, $A8, $FB, $A9, $FF, $AA, $05 ; <<<<<< CHANGE THIS EVENT

    ; default case
    db $FF, $00, $00

; STEAMSHIP CATAPULT LOCK

; new code area for conditional checking. EACH X/Y CHECKER HAS A CORRESPONDING OUTPUT HERE
; org $D8FFA8
org $F06004

; Simple example, does not allow for directional confirm for something like a door
; db !keyitemarea, $FF, $4C, $00, $FF, $F0, $00

; Complex example, checks each direction first and nulls event, but if it's the matching direction, proceed with conditionals for checking key item flag then running event 

db $F7, $00, $FF, $65, $03














; X Y CUSTOM COORDINATES

org $CE3660
; submarine in world 2 for new access area

db $70, $65, $13, $00
db $39, $41, $2e, $00
db $A9, $A4, $5A, $00

; ; Lonka Rift
org $CE3670
db $0C, $2E, $7d, $02
; ; Falls Rift
org $CE3674
db $2C, $38, $7d, $02
; ; Castle Rift
org $CE3678
db $16, $2C, $7d, $02

; ; Shoat Cave
org $CE367C
db $17, $24, $7a, $00
db $0E, $1D, $00, $00

; ; Portal Boss
org $CE3684
db $08, $0A, $00, $00





; ; World map steamship
org $CE3688
db $54, $4F, $00, $11

; ; Rift castle door
org $CE368C
db $06, $28, $00, $00

; I decided to make a custom solution by making a new table entirely for offsets here
; the above $00, $11 places data in an entirely new blank area (0x1100 times 2 offset from F04000)
; puts data at $F06200 

org $F06200
; this puts the actual conditional code location
; as opposed to above, this is not times 2. So, direct from F04000
db $20, $22, $23, $22

; this is conditional code
org $F06220
db $FF, $6C, $00










; XY Coordinate hook
org $C00654
JML XYCoordinateHook

org !ADDRESS_xycoordhook
XYCoordinateHook:


; Submarine world 2
lda !mapid
CMP #$0003
BNE XYCoordinateHookContinueCase2
lda !xycoordcheck
CMP #$A4A9
BNE XYCoordinateHookContinueCase2

; IF these match, we're in submarine in world 2, so set up coordinates specifically
LDA #$6012
STA $23
LDA #$6B12
STA $26
; Set an event flag for submarine handling in 8 bit mode

phx
sep #$20
LDA #$02
LDX #$002C
JSL SetKeyItemBits
rep #$20
plx
JMP XYCoordinateHookContinueNormalCase
XYCoordinateHookContinueCase2:



; LONKA RIFT 
lda !mapid
CMP #$01DF
BNE XYCoordinateHookContinueCase3
lda !xycoordcheck
CMP #$2E0C
BNE XYCoordinateHookContinueCase3

; IF these match, set up coordinates specifically
LDA #$1270
STA $26
TAX
LDA #$1274
STA $23

JMP XYCoordinateHookContinueNormalCase

XYCoordinateHookContinueCase3:
; FALLS RIFT 
lda !mapid
CMP #$01EC
BNE XYCoordinateHookContinueCase4
lda !xycoordcheck
CMP #$382C
BNE XYCoordinateHookContinueCase4

; IF these match, set up coordinates specifically
LDA #$1274
STA $26
TAX
LDA #$1278
STA $23

JMP XYCoordinateHookContinueNormalCase

XYCoordinateHookContinueCase4:
; CASTLE RIFT 
lda !mapid
CMP #$01F0
BNE XYCoordinateHookContinueCase5
lda !xycoordcheck
CMP #$2C16
BNE XYCoordinateHookContinueCase5

; IF these match, set up coordinates specifically
LDA #$1278
STA $26
TAX
LDA #$127C
STA $23

JMP XYCoordinateHookContinueNormalCase

XYCoordinateHookContinueCase5:
; ; SHOAT CAVE
lda !mapid
CMP #$01AC
BNE XYCoordinateHookContinueCase6
lda !xycoordcheck
CMP #$1D0E
BNE XYCoordinateHookContinueCase6

; ; IF these match, set up coordinates specifically
LDA #$127C
STA $26
TAX
LDA #$1284
STA $23
JMP XYCoordinateHookContinueNormalCase
XYCoordinateHookContinueCase6:

; mapid $2101
; xy $080a


; ; PORTAL BOSS
lda !mapid
CMP #$0121
BNE XYCoordinateHookContinueCase7
lda !xycoordcheck
CMP #$0A08
BNE XYCoordinateHookContinueCase7

; ; IF these match, set up coordinates specifically
LDA #$1284
STA $26
TAX
LDA #$1288
STA $23
JMP XYCoordinateHookContinueNormalCase
XYCoordinateHookContinueCase7:

; ; STEAMSHIP WORLD MAP
lda !mapid
CMP #$0000
BNE XYCoordinateHookContinueCase8
lda !xycoordcheck
CMP #$4F54
BNE XYCoordinateHookContinueCase8

; then do a event flag check 

; for archipelago, skip this logic check - always allow access back to steamship
; lda $0A1A
; and #$0001
; BNE XYCoordinateHookContinueNormalCase


; ; IF these match, set up coordinates specifically
LDA #$1288
STA $26
TAX
LDA #$128C
STA $23
JMP XYCoordinateHookContinueNormalCase
XYCoordinateHookContinueCase8:





; ; RIFT CASTLE DOOR
lda !mapid
CMP #$01F5
BNE XYCoordinateHookContinueCase9
lda !xycoordcheck
CMP #$2806
BNE XYCoordinateHookContinueCase9



; ; IF these match, set up coordinates specifically
LDA #$128C
STA $26
TAX
LDA #$1290
STA $23
JMP XYCoordinateHookContinueNormalCase
XYCoordinateHookContinueCase9:









XYCoordinateHookContinueNormalCase:
cpx $23
beq XYCoordinateHookBaseCase1
LDA $ce2400,x
lda $0ad8
cmp $ce2400,x
beq XYCoordinateHookBaseCase2
txa
clc
adc #$0004
tax
jml XYCoordinateHookReplicated  ; after checked once for xy coords, now replicate original code entirely

XYCoordinateHookBaseCase1:
JML $C00681
XYCoordinateHookBaseCase2:
JML $C0066a


XYCoordinateHookReplicated:
; replicate original code. 
cpx $23
beq XYCoordinateHookBaseCase1
lda $0ad8
cmp $ce2400,x
beq XYCoordinateHookBaseCase2
txa
clc
adc #$0004
tax
jml !ADDRESS_xycoordhook  ; this will loop until another case is hit


































; Key item hook for custom warp tiles/event triggering
org $C0046C
JML KeyItemLockingHook

org !ADDRESS_keyitemlocks
KeyItemLockingHook:
LDA !RELOCATE_conditional_events,x 
STA $23
LDA !RELOCATE_conditional_events+2, X
STA $26

; case by case - when condition met, manually change loaded in values
; THIS IS STILL IN 16 BIT A MODE
; check map ID
; sep #$20 = 8 bit 
; rep #$20 = 16 bit 




; WORLD MAP STEAMSHIP ACCESS
lda !mapid
CMP #$009C
BNE KeyItemLockingNextCheck1
lda !xycoordcheck
CMP #$110C
BNE KeyItemLockingNextCheck1

; HANDLE STEAMSHIP
LDA #$1F28
STA $23
LDA #$1F41
STA $26
JMP KeyItemLockingImmediateFinish






KeyItemLockingNextCheck1:

; BIG BRIDGE ACCESS (SOUTH)
lda !mapid
CMP #$013C
BNE KeyItemLockingNextCheck1point5
lda !xycoordcheck
CMP #$0B0D
BNE KeyItemLockingNextCheck1point5

; HANDLE BIG BRIDGE
LDA #$1F42
STA $23
LDA #$1F4A
STA $26
JMP KeyItemLockingImmediateFinish

KeyItemLockingNextCheck1point5:
; BIG BRIDGE ACCESS (NORTH)
lda !mapid
CMP #$013C
BNE KeyItemLockingNextCheck2
lda !xycoordcheck
CMP #$122F
BNE KeyItemLockingNextCheck2

; HANDLE BIG BRIDGE
LDA #$1F4A
STA $23
LDA #$1F52
STA $26
JMP KeyItemLockingImmediateFinish





KeyItemLockingNextCheck2:




; SUBMARINE BARRIER TOWER ACCESS
lda !mapid
CMP #$0003
BNE KeyItemLockingNextCheck3
lda !xycoordcheck
CMP #$A4A9
BNE KeyItemLockingNextCheck3

; HANDLE BARRIER TOWER ACCESS


LDA #$1F52
STA $23
LDA #$1F56
STA $26
JMP KeyItemLockingImmediateFinish



KeyItemLockingNextCheck3:

; SOLITARY SHRINE ACCESS
lda !mapid
CMP #$0183
BNE KeyItemLockingNextCheck4
lda !xycoordcheck
CMP #$3A15
BNE KeyItemLockingNextCheck4

; HANDLE SOLITARY SHRINE ACCESS

LDA #$1F56
STA $23
LDA #$1F63
STA $26
JMP KeyItemLockingImmediateFinish



KeyItemLockingNextCheck4:


; TRENCH ACCESS
lda !mapid
CMP #$019E
BNE KeyItemLockingNextCheck5
lda !xycoordcheck
CMP #$2E13
BNE KeyItemLockingNextCheck5

; HANDLE TRENCH ACCESS

LDA #$1F63
STA $23
LDA #$1F70
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck5:



; FALLS ACCESS
lda !mapid
CMP #$01A6
BNE KeyItemLockingNextCheck6
lda !xycoordcheck
CMP #$2715
BNE KeyItemLockingNextCheck6

; HANDLE FALLS ACCESS

LDA #$1F70
STA $23
LDA #$1F7D
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck6:




; PYRAMID RIFT ACCESS
lda !mapid
CMP #$01DC
BNE KeyItemLockingNextCheck7
lda !xycoordcheck
CMP #$0E35
BNE KeyItemLockingNextCheck7

; HANDLE PYRAMID RIFT ACCESS

LDA #$1F80
STA $23
LDA #$1F94
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck7:





; LONKA RIFT ACCESS
lda !mapid
CMP #$01DF
BNE KeyItemLockingNextCheck8
lda !xycoordcheck
CMP #$2E0C
BNE KeyItemLockingNextCheck8

; HANDLE LONKA RIFT ACCESS

LDA #$1F80
STA $23
LDA #$1F94
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck8:




; FALLS RIFT ACCESS
lda !mapid
CMP #$01EC
BNE KeyItemLockingNextCheck9
lda !xycoordcheck
CMP #$382C
BNE KeyItemLockingNextCheck9

; HANDLE FALLS RIFT ACCESS

LDA #$1F80
STA $23
LDA #$1F94
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck9:





; CASTLE RIFT ACCESS
lda !mapid
CMP #$01F0
BNE KeyItemLockingNextCheck10
lda !xycoordcheck
CMP #$2C16
BNE KeyItemLockingNextCheck10

; HANDLE CASTLE RIFT ACCESS

LDA #$1F80
STA $23
LDA #$1F95
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck10:


; TORNA CANAL ACCESS
lda !mapid
CMP #$0028
BNE KeyItemLockingNextCheck11
lda !xycoordcheck
CMP #$2235
BNE KeyItemLockingNextCheck11

; HANDLE TORNA CANAL ACCESS

LDA #$1F95
STA $23
LDA #$1FA0
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck11:

; SHOAT CAVE ACCESS
lda !mapid
CMP #$01AC
BNE KeyItemLockingNextCheck12
lda !xycoordcheck
CMP #$1D0E
BNE KeyItemLockingNextCheck12

; HANDLE SHOAT CAVE ACCESS

LDA #$1FA0
STA $23
LDA #$1FCB
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck12:


; PHOENIX CAVE VALIDATION
lda !mapid
CMP #$01B2
BNE KeyItemLockingNextCheck13
lda !xycoordcheck
CMP #$160F
BNE KeyItemLockingNextCheck13

; HANDLE PHOENIX CAVE VALIDATION

LDA #$1FCB
STA $23
LDA #$1FDF
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck13:


; PORTAL BOSS VALIDATION
lda !mapid
CMP #$0121
BNE KeyItemLockingNextCheck14
lda !xycoordcheck
CMP #$0A08
BNE KeyItemLockingNextCheck14

; HANDLE PORTAL BOSS VALIDATION

LDA #$1FDF
STA $23
LDA #$2002
STA $26
JMP KeyItemLockingImmediateFinish
KeyItemLockingNextCheck14:


; STEAMSHIP CATAPULT ACCESS
lda !mapid
CMP #$00D2
BNE KeyItemLockingNextCheck15
lda !xycoordcheck
CMP #$110C
BNE KeyItemLockingNextCheck15

; HANDLE STEAMSHIP CATAPULT
LDA #$2004
STA $23
LDA #$2009
STA $26
JMP KeyItemLockingImmediateFinish

KeyItemLockingNextCheck15:



; RIFT CASTLE DOOR ACCESS
lda !mapid
CMP #$01F5
BNE KeyItemLockingNextCheck16
lda !xycoordcheck
CMP #$2806
BNE KeyItemLockingNextCheck16

; HANDLE RIFT CASTLE DOOR
LDA #$2009
STA $23
LDA #$2013
STA $26
JMP KeyItemLockingImmediateFinish

KeyItemLockingNextCheck16:










KeyItemLockingReplicateOriginal:
LDA !RELOCATE_conditional_events,x 
STA $23
LDA !RELOCATE_conditional_events+2, X
STA $26

KeyItemLockingImmediateFinish:
JML $C00478




; fix all references to [D8E080,x] to [!RELOCATE_conditional_events,x]

org $C0047F
db !RELOCATE_conditional_events_le
; FC
org $C004B2
db !RELOCATE_conditional_events_le_offset1
; FF
org $C00607
db !RELOCATE_conditional_events_le_offset1
org $C0048E
db !RELOCATE_conditional_events_le_offset1
org $C005E9
db !RELOCATE_conditional_events_le
org $C004A0
db !RELOCATE_conditional_events_le_offset1
org $C004C4
db !RELOCATE_conditional_events_le_offset1
org $C004E1
db !RELOCATE_conditional_events_le_offset1
org $C005CE
db !RELOCATE_conditional_events_le_offset1
org $C005DD
db !RELOCATE_conditional_events_le_offset3
org $C00523
db !RELOCATE_conditional_events_le_offset1
org $C0052A
db !RELOCATE_conditional_events_le_offset1
org $C0057A
db !RELOCATE_conditional_events_le_offset1
org $C005A6
db !RELOCATE_conditional_events_le_offset1
org $C004ED
db !RELOCATE_conditional_events_le_offset2
org $C004F8
db !RELOCATE_conditional_events_le_offset3
org $C00514
db !RELOCATE_conditional_events_le_offset3

; remove the crutch of old code and hope for the best

org $D8E080
pad $D90000







; This event is the submarine leaving barrier tower
org $C98882
db $E0, $03, $20, $A9, $A5, $91
db $A3, $C1            ; set address 000A2C bit OFF 02
db $FF                          ;End Event
pad $C988F4