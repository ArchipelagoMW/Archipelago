hirom

org $c2a37b
jml $f00d80

org $f00d80

; first check which menu we're on at all
lda $0143
cmp #$01
beq PreCheckFourJobRequirements 

; if it fails, normal case

; THIS IS NORMAL UNEDITED CASE
NormalCaseLeaveMenu:
lda $54
rep #$20
and #$007F
asl a
asl a
inc
inc
tax
jml $c2a387


; THIS IS FOR REJECTING INPUT
; IT ACTUALLY JUST WORKS
; SO YOU USE THIS WHEN YOU REJECT
; ON VERY SPECIFIC CONDITIONS?
; BOTH ON MENU CONDITIONS OF BEING
; THE MAIN MENU
; BUT THEN ALSO ON 4 JOB CRITERIA

PreCheckFourJobRequirements:
; criteria 2
lda $0157
cmp #$00
beq CheckFourJobRequirements
cmp #$01
beq CheckFourJobRequirements
bne NormalCaseLeaveMenu

CheckFourJobRequirements:
; now formally check 4 jobs
JSL FourJobSubroutineCheck
CMP #$01 ; success case
BEQ NormalCaseLeaveMenu
BNE CheckFourJobRequirementsFailure

CheckFourJobRequirementsFailure:
rep #$20
lda #$A4F0
sep #$20
jml $c2a4f0






FourJobSubroutineCheck:
; returns A value of 
; 00 = Failure
; 01 = Success

; Check each character first to see if they're hidden
; If so, automatically pass test


lda $0500
AND #$40
BNE FourJobSubroutineCheckPass
lda $0550
AND #$40
BNE FourJobSubroutineCheckPass
lda $05A0
AND #$40
BNE FourJobSubroutineCheckPass
lda $05F0
AND #$40
BNE FourJobSubroutineCheckPass


; if made it past these, then start checking actual jobs
; and if no active jobs are shared among party members

lda $0501
cmp $0551
beq DisallowMenuLeaving
cmp $05A1
beq DisallowMenuLeaving
cmp $05F1
beq DisallowMenuLeaving

; 2nd job
lda $0551
cmp $05A1
beq DisallowMenuLeaving
cmp $05F1
beq DisallowMenuLeaving

; 3rd job
lda $05A1
cmp $05F1
beq DisallowMenuLeaving

; if all conditions met, then allow leaving
FourJobSubroutineCheckPass:
LDA #$01
RTL 

DisallowMenuLeaving:

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

; Failure condition = $00
lda #$00
RTL







; 0157 = $00 or $01, on MAIN menu
; 0143 = $01