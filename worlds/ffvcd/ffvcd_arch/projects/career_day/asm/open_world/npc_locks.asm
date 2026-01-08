hirom

org $C02F9C
JML !ADDRESS_NPC_LOCKS

org !ADDRESS_NPC_LOCKS

; manually check for odin location
lda !mapid
CMP #$0118
BNE NPCLockOriginalExit
lda !xycoordcheck
CMP #$0708
BNE NPCLockOriginalExit

; if a match, set up and jump out
LDA #$22A0
sta $23
sta $29
LDA #$22A9
sta $26
lda $06
JML $C02FAC




NPCLockOriginalExit:
lda $ce0000,x
sta $23
sta $29
lda $ce0002,x
sta $26
lda $06
JML $C02FAC


