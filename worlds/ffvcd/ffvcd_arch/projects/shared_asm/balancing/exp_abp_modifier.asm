hirom

; change config to only allow for 4 options
org $C0F078
db $03 ; change 'too far' metric



; org $C23F8E

; JML EXPHook

; org !ADDRESS_expmod
; EXPHook:

; ; This code below was only changing the first enemy for rewards. Don't think there's a reason to use it, keeping here just in case. 
; ; CPY #$0000
; ; BNE FinishEXPHookImmediate

; ; Load reward config 
; LDA #$0000
; sep #$20
; LDA !rewardconfig
; and #$70
; CMP #$20
; BEQ EXPMult4
; CMP #$10
; BEQ EXPMult2
; ; no config
; JMP FinishEXPHookImmediate


; EXPMult2:
; rep #$20
; lda $3F0B, x
; asl
; JMP FinishExpReward
; EXPMult4:
; rep #$20
; lda $3F0B, x
; asl
; asl
; JMP FinishExpReward


; FinishExpReward:

; ; check to make sure overflow did not happen 


; sta $2267,y
; JML $C23F94

; FinishEXPHookImmediate:
; rep #$20
; lda $3F0B, x
; sta $2267,y
; JML $C23F94


org $c257f4

JML EXPHook

org !ADDRESS_expmod
EXPHook:
; first check if overflow happened, if so, set max and move on
LDA $7E7C10
CMP #$00 
BEQ EXPContinue

; if overflow happened, set to max and leave
LDA #$00
STA $7E7C10
rep #$20
LDA #$FFFF
STA $7E7C0E
JMP FinishExpReward

EXPContinue:
; to be sure, zero out overflow so <65535
LDA #$00
STA $7E7C10
; Load reward config 
sep #$20
LDA !rewardconfig
and #$70
CMP #$20
BEQ EXPMult4
CMP #$10
BEQ EXPMult2
; no config
JMP FinishExpReward



EXPMult2:
lda $7e7c0f
SBC #$80
bcc EXPMult2PerformASL
; if greater than 40, do not apply mult and set to max
rep #$20
LDA #$FFFF
STA $7E7C0E
JMP FinishExpReward

EXPMult2PerformASL:
rep #$20
lda $7e7c0e
asl
sta $7e7c0e
JMP FinishExpReward


EXPMult4:
lda $7e7c0f
SBC #$40
bcc EXPMult4PerformASL

; if carry was set, do not apply mult and set to max
rep #$20
LDA #$FFFF
STA $7E7C0E
JMP FinishExpReward

EXPMult4PerformASL:
rep #$20
lda $7e7c0e
asl
asl
sta $7e7c0e
JMP FinishExpReward


FinishExpReward:
sep #$20
ldx $7c0e
stx $0e
lda $7c10
JML $c257fc


















org $C24D27
JML ABPHook

org !ADDRESS_abpmod
ABPHook:
; TYA
CPY #$0002
BNE FinishABPHookImmediate

; Load reward config 
LDA !rewardconfig
and #$70
CMP #$20
BEQ ABPMult4
CMP #$10
BEQ ABPMult2
; no config
JMP FinishABPHookImmediate




ABPMult2:
CLC
lda $d03000,x
asl
BCS LoadMaxABP
JMP FinishABPReward
ABPMult4:
CLC
lda $d03000,x
asl
BCS LoadMaxABP
asl
BCS LoadMaxABP
JMP FinishABPReward

LoadMaxABP:
lda #$FF

FinishABPReward:
sta $3eef,y
JML $C24D2E

FinishABPHookImmediate:

lda $d03000,x
sta $3eef,y
JML $C24D2E