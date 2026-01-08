hirom


; DESTINATION : Code $CC
; new event handler is going to be $CC with 1 operand argument

org $C0A580 ; new offset for generic event handler
db $90, $CD ; this will make the new loading code for this $C0CD90

org $C0CD90
lda $DF ; load in argument 
sta !destinationindex
JMP $A630




; REWARDS : Code $DE
; Apparently free space in area C0FAB0, used here for event reward indexing 

org $C0A5A4 ; new offset for generic event handler
db $A0, $CD ; this will make the new loading code for this $C0CDA0

org $C0CDA0
pha
phx
phy


; lda $DF ; load in first argument, which will be the reward index.
; asl ; asl it once, because we'll be indexing for every 2 bytes for reward type and id
; tax

rep #$20
lda #$0000
sep #$20
lda $DF ; load in first argument, which will be the reward index.
rep #$20
asl ; asl it once, because we'll be indexing for every 2 bytes for reward type and id
tax
lda #$0000
sep #$20

lda !eventrewardindex+1, x ; load in reward id 
sta !rewardid
sta !nonmagicrewardindex				; another reward id
lda !eventrewardindex, x ; load in type id 
sta !typeid

CMP #$40 ; compare type id
BEQ EventRewardItem
CMP #$30 ; compare type id
BEQ EventRewardKeyItem
CMP #$20 ; compare type id
BEQ EventRewardMagic
CMP #$50 ; compare type id 
BEQ EventRewardCrystal
CMP #$60 ; compare type id
BEQ EventRewardAbility

JMP FinishRewardEvent ; in case no matches


EventRewardItem: ; give item
lda !rewardid
sta !nonmagicrewardindex				; another reward id
jsr $bfdd ; this subroutine handles awarding item based on cycling through inventory
cpy #$0100 ; if 100 was reached (255 items), then award new item
BEQ AwardNewItem

; item was found, award it
lda $0740, y
cmp #$63
BEQ FinishRewardEvent ; if 99, don't add again, finish event 
; otherwise award item 
lda $0740, y
inc
sta $0740, y
JMP FinishRewardEvent




; no new item was reached, add an entirely new one 
AwardNewItem:
ldy $06
AwardNewItem2:
lda $0640,y
BEQ BlankSlotFound
iny
BRA AwardNewItem2

BlankSlotFound:
lda !nonmagicrewardindex
sta $0640,y
lda #$01
sta $0740,y
JMP FinishRewardEvent







EventRewardKeyItem: ; give key item
JSL BranchToKeyItemReward
JMP FinishRewardEvent


EventRewardMagic: ; give magic
if !progressive = 0
	lda $12
    sta $16a3
else
    JSL BranchToMagicReward
endif
jsr $C9A5
JMP FinishRewardEvent

EventRewardCrystal:
JSL BranchToJobReward
JMP FinishRewardEvent

EventRewardAbility:
JSL BranchToAbilityReward
JMP FinishRewardEvent

FinishRewardEvent:
ply
plx
pla 
;sta !destinationindex
JML $C0A630



; Ran into space issues
; For the base case 







; REWARD TEXT BOX SWITCHER : Code $DF

; Here, we have separate text boxes for All-non magic rewards, and all-magic rewards
; So we used the reward type ID loaded in from event code $DE to distinguish which textbox to use
; This system is cleverly advancing the 'event code index' ($D6) and hardcoding in the textbox to use for either magic or non-magic (Either C8 04 00 or C8 02 00 into arguments $E0, $DF, and $DE)

org $C0A5A6 ; new offset for generic event handler
db $A0, $CE ; this will make the new loading code for this $C0CD9A0

org $C0CEA0

; set up text, first and third operand always the same 
dec $D6 ; offset index by one
dec $D6 ; offset index by one
lda #$C8
STA $DE	; mimic dialogue event $C8 as first operand
LDA #$00 
STA $E0 ; mimic second argument (third operand) for dialogue

lda !typeid
CMP #$20
BEQ MagicTextBox

; standard text box
lda #$02
sta $DF
JMP $C7A4 ; branch the fk out and hope it works

; magic text box
MagicTextBox:
lda #$04
sta $DF 
JMP $C7A4 ; branch the fk out and hope it works (it does)



; RANDOMIZER JOB SETTING  : Code $EC
; On rando seeds, this will trigger from the values written to E79F00:
; $00 = job id

org $C0A5C0
db $F0, $CE ; branch to $C0CE20

org $C0CEF0
JML RandomizerJobSetting

org !ADDRESS_NEWEVENT_jobsetting
; This process will be VERY different for Four Job mode, so entirely changing
; the code on conditional

if !fourjobmode == 0
; #####################
; # NORMAL MODE
; #####################
    RandomizerJobSetting:
    pha
    phx



    ; turn off freelancer
    LDA #$00
    STA $000842

    ; set control to zero for name validation (phoenix tower)
    STA !charnamecontrol


    ; set job value to learned jobs
    LDX #$0000
    LDA $E79F00
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F00
    lsr
    lsr
    lsr
    tax
    pla
    ora $0840,x
    sta $0840,x

    ; set everyone to have 1 ability count from the start
    lda #$01
    sta $08F3
    sta $08F4
    sta $08F5
    sta $08F6

    ; start data move for stats
    rep #$20
    lda #$0000
    sep #$20
    lda $E79F00
    rep #$20
    asl
    TAX
    LDA #$0500
    TAY
    LDA $F80F00, X
    XBA
    TAX

    LDA #$013F
    MVN $F800

    LDA #$0000
    sep #$20

    ; set starting magic
    LDA $E79F01
    CMP #$FF
    BEQ RandomizedJobSkipMagic
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F01
    lsr
    lsr
    lsr
    tax
    pla
    ora $0950,x
    sta $0950,x

    RandomizedJobSkipMagic:

    plx
    pla

    JML $C0A628 ; hopefully this works 

elseif !fourjobmode == 1
; #####################
; # FOUR JOB MODE
; #####################
    RandomizerJobSetting:
    pha
    phx

    ; turn off freelancer
    LDA #$00
    STA $000842

    ; set control to zero for name validation (phoenix tower)
    STA !charnamecontrol

    ; set job value to learned jobs
    LDX #$0000
    LDA $E79F00
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F00
    lsr
    lsr
    lsr
    tax
    pla
    ora $0840,x
    sta $0840,x

    ; job2
    LDX #$0000
    LDA $E79F02
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F02
    lsr
    lsr
    lsr
    tax
    pla
    ora $0840,x
    sta $0840,x

    ; job3
    LDX #$0000
    LDA $E79F04
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F04
    lsr
    lsr
    lsr
    tax
    pla
    ora $0840,x
    sta $0840,x

    ; job4
    LDX #$0000
    LDA $E79F06
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F06
    lsr
    lsr
    lsr
    tax
    pla
    ora $0840,x
    sta $0840,x

    ; set everyone to have 1 ability count from the start
    lda #$01
    sta $08F3
    sta $08F4
    sta $08F5
    sta $08F6

    ; start data move for stats
    rep #$20
    lda #$0000
    sep #$20
    lda $E79F00
    rep #$20
    asl
    TAX
    LDA #$0500
    TAY
    LDA $F80F00, X
    XBA
    TAX
    LDA #$004F
    MVN $F800

    ; job2
    rep #$20
    lda #$0000
    sep #$20
    lda $E79F02
    rep #$20
    asl
    TAX
    LDA #$0550
    TAY
    LDA $F80F00, X
    XBA
    ; offset by char #
    STA $1F08 ; SCRATCH RAM
    LDA #$0050
    ADC $1F08    
    TAX

    LDA #$004F
    MVN $F800
    
    ; job3
    rep #$20
    lda #$0000
    sep #$20
    lda $E79F04
    rep #$20
    asl
    TAX
    LDA #$05A0
    TAY
    LDA $F80F00, X
    XBA
    ; offset by char #
    STA $1F08; SCRATCH RAM
    LDA #$00A0
    ADC $1F08    
    TAX
    LDA #$004F
    MVN $F800

    ; job4
    rep #$20
    lda #$0000
    sep #$20
    lda $E79F06
    rep #$20
    asl
    TAX
    LDA #$05F0
    TAY
    LDA $F80F00, X
    XBA
    ; offset by char #
    STA $1F08; SCRATCH RAM
    LDA #$00F0
    ADC $1F08
    TAX

    LDA #$004F
    MVN $F800

    LDA #$0000
    sep #$20


    ; ; set starting magic
    LDA $E79F01
    CMP #$FF
    BEQ RandomizedJobSkipMagic1
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F01
    lsr
    lsr
    lsr
    tax
    pla
    ora $0950,x
    sta $0950,x

    RandomizedJobSkipMagic1:
    
    LDA $E79F03
    CMP #$FF
    BEQ RandomizedJobSkipMagic2
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F03
    lsr
    lsr
    lsr
    tax
    pla
    ora $0950,x
    sta $0950,x

    RandomizedJobSkipMagic2:
    
    
    LDA $E79F05
    CMP #$FF
    BEQ RandomizedJobSkipMagic3
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F05
    lsr
    lsr
    lsr
    tax
    pla
    ora $0950,x
    sta $0950,x

    RandomizedJobSkipMagic3:
    
    
    LDA $E79F07
    CMP #$FF
    BEQ RandomizedJobSkipMagic4
    AND #$07
    tax
    LDA $C0C9B9,X
    pha
    LDA $E79F07
    lsr
    lsr
    lsr
    tax
    pla
    ora $0950,x
    sta $0950,x

    RandomizedJobSkipMagic4:

    plx
    pla

    JML $C0A628 ; hopefully this works 


endif



; CONDITIONAL VEHICLE PLACEMENT : Code $ED
; Based on whether certain event flags are set, place/do not place vehicles

org $C0A5C2
db $F4, $CE ; branch to $C0CE20

org $C0CEF4
JML ConditionalVehicles

org !ADDRESS_NEWEVENT_conditionalvehicles
ConditionalVehicles:

; check vehicle type
LDY #$0004 ; offset for how far into $D2 command for vehicle type
LDA [$D6], y
; SUBMARINE
CMP #$6C ; submarine code
BNE ConditionalVehiclesCheckHiryuu
LDA $000A4A
AND #$04 ; 000A4A, test bit 04
CMP #$04
BEQ ConditionalVehiclesPlaceVehicle
BNE ConditionalVehiclesFailure



JMP ConditionalVehiclesPlaceVehicle


ConditionalVehiclesCheckHiryuu:
; check vehicle type
LDY #$0004 ; offset for how far into $D2 command for vehicle type
LDA [$D6], y
; HIRYUU
CMP #$90 ; hiryuu code
BNE ConditionalVehiclesFailure
LDA $000A4A
AND #$02 ; 000A4A, test bit 02
CMP #$02
BEQ ConditionalVehiclesPlaceVehicle
BNE ConditionalVehiclesFailure

; replicate original code, but manually set #$D2 at the end to place vehicle
ConditionalVehiclesPlaceVehicle:
STZ $BA
LDX $D4
LDY #$0005
LDA [$D6], y
STA $E3
DEY
LDA [$D6], y
STA $E2
DEY
LDA [$D6], y
STA $E1
DEY
LDA [$D6], y
STA $E0
DEY
LDA [$D6], y
STA $DF
DEY
LDA #$D2
STA $DE
JML $C0A26C


ConditionalVehiclesFailure:
; failure
LDA $D6
ADC #$05
STA $D6
JML $C0A248



; CONDITIONAL EVENT FLAGS ON WARP : Code $EE
; Based on whether certain event flags are set, change event flags. Primarily for vehicles
; And changing worlds. Also Ronka access 


org $C0A5C4
db $F8, $CE ; branch to $C0CE20

org $C0CEF8
JML ConditionalEventFlags

org !ADDRESS_NEWEVENT_conditionaleventflags
ConditionalEventFlags:

; no matter what, treat these flags:

; flag for leaving the Rift (important for Exit spell, otherwise Rift exit spell cutscene plays and places player in w3)
; LDA #$00
; STA $0AFB


LDA #$01
TRB $0A14

; load world
LDA $000AD6
CMP #$00
BNE ConditionalEventFlagsCheckWorld2
; World 1
; Set RONKA RUINS access to on IF Adamantite active
LDA $000A4C
AND #$04
CMP #$04
BNE ConditionalEventFlagsCheckWorld1Next1 
; Condition met 
phx
LDA #$04
LDX #$0053
JSL SetKeyItemBits
plx

ConditionalEventFlagsCheckWorld1Next1:

JMP ConditionalEventFlagsFinish

ConditionalEventFlagsCheckWorld2:
LDA $000AD6
CMP #$01
BNE ConditionalEventFlagsCheckWorld3


ConditionalEventFlagsCheckWorld3:
LDA $000AD6
CMP #$02
BNE ConditionalEventFlagsFinish
; Set SUBMARINE ON AIRSHIP if SUBMARINE KEY
LDA $000A4A
AND #$02
CMP #$02
BNE ConditionalEventFlagsCheckWorld3Next1 
; Condition met
phx
LDA #$02
LDX #$0053
JSL SetKeyItemBits
plx
ConditionalEventFlagsCheckWorld3Next1:

ConditionalEventFlagsFinish:
JML $C0A628 ; hopefully this works 




; RIFT TABLET COUNTING : Code $EF
; Checks 4 tablets and gets a count
; Then checks map ID for position and determine if player belongs or not
; Uses unused event flag 

org $C0A5C6
db $FC, $CE ; branch to $C0CE20

org $C0CEFC
JML RiftTabletConditional

org !ADDRESS_NEWEVENT_conditionalrifttablet
RiftTabletConditional:
STZ !unusedram1
STZ !unusedram2


; Get count of how many tablets 
; 1st tablet
LDA $0A4D
AND #$20
CMP #$20
BNE CheckNextTablet2
INC !unusedram1

CheckNextTablet2:
; 2nd tablet
LDA $0A4D
AND #$10
CMP #$10
BNE CheckNextTablet3
INC !unusedram1

CheckNextTablet3:
; 3rd tablet
LDA $0A4D
AND #$04
CMP #$04
BNE CheckNextTablet4
INC !unusedram1

CheckNextTablet4:
; 4th tablet
LDA $0A4D
AND #$08
CMP #$08
BNE RiftTabletContinue1
INC !unusedram1

RiftTabletContinue1:

; Check map id, 1 byte's enough
lda $0AD4
; Pyramid area, 1st check
CMP #$DC
BNE CheckNextRiftMap1
LDA #$01
JMP RiftTabletContinue2
CheckNextRiftMap1:
; Lonka area, 2nd check
CMP #$DF
BNE CheckNextRiftMap2
LDA #$02
JMP RiftTabletContinue2
CheckNextRiftMap2:
; Falls area, 3rd check
CMP #$EC
BNE CheckNextRiftMap3
LDA #$03
JMP RiftTabletContinue2
CheckNextRiftMap3:
; Castle area, 4th check
CMP #$F0
BNE RiftTabletContinue2
LDA #$04



RiftTabletContinue2:
STA !unusedram2
LDA !unusedram1
; A has now has count of tablets, !unusedram2 has value to check against per map
CMP !unusedram2
; Branch if carry clear means A is less than the count per the map ID
BCC RiftTabletFailureCase

; Success case - A42 to 01
LDA #$00
STA !unusedram1
STA !unusedram2
LDA #$01
LDX #$0041
JSL SetKeyItemBits
; This marks the event as complete for conditional branchhing
LDA #$02
LDX #$0041
JSL SetKeyItemBits
JML $C0A628 ; end event function

RiftTabletFailureCase:
LDA #$00
STA !unusedram1
STA !unusedram2
LDA #$01
TRB $0A41
; Failure case - A42 set to 02 only
LDA #$02
LDX #$0041
JSL SetKeyItemBits
JML $C0A628 ; end event function



; Unused, saved for syntax
;; RONKA RUINS always unset
; LDA #$04
; TRB $0A53




; NAME INPUT VALIDATER : Code $F2
org $C0A5CC 
db $38, $CE 

org $C0CE38
JML !ADDRESS_NEWEVENT_namevalidation

org !ADDRESS_NEWEVENT_namevalidation
lda !charnamecontrol
CMP #$01
BEQ CharNameControlOn
; Control off - save name, set it to on and branch
LDA $0990
STA !charname1
LDA $0991
STA !charname2
LDA $0992
STA !charname3
LDA $0993
STA !charname4
LDA $0994
STA !charname5
LDA $0995
STA !charname6

LDA #$01
STA !charnamecontrol
JMP CharNameValidationFinish

; Control on - compare each byte to !ADDRESS_phoenixtowername and set !charnamepass if so
; Then always restore original name & set control off
CharNameControlOn:
LDA $0990
CMP !ADDRESS_phoenixtowername
BNE FinishControlOn
LDA $0991
CMP !ADDRESS_phoenixtowername+1
BNE FinishControlOn
LDA $0992
CMP !ADDRESS_phoenixtowername+2
BNE FinishControlOn
LDA $0993
CMP !ADDRESS_phoenixtowername+3
BNE FinishControlOn
LDA $0994
CMP !ADDRESS_phoenixtowername+4
BNE FinishControlOn
LDA $0995
CMP !ADDRESS_phoenixtowername+5
BNE FinishControlOn
; if it made it this far, the name passed, so set the event code bit

LDA #$08
TSB $0A20

FinishControlOn:
LDA !charname1
STA $0990
LDA !charname2
STA $0991
LDA !charname3
STA $0992
LDA !charname4
STA $0993
LDA !charname5
STA $0994
LDA !charname6
STA $0995


LDA #$00
STA !charnamecontrol







CharNameValidationFinish:
JML $C0A628 ; hopefully this works 


