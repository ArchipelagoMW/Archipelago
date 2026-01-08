hirom

; WORKS FINE, this will trigger actively in battle


; code for instant death 
; org $C1000E
; JML BattleHook

; org !ADDRESS_battlehook
; BattleHook:

; rep #$20
; pha
; lda !input
; cmp #$2060 ; L X Select
; BEQ BattleHookAnnihilate
; BNE BattleHookFinish

; ; if condition met, set characters dead
; BattleHookAnnihilate:
; sep #$20
; LDA #$40
; sta $201A
; sta $209A
; sta $211A
; sta $219A
; rep #$20

; ; original code
; BattleHookFinish:
; pla
; sep #$20
; LDA $C10021,X
; STA $7A
; LDA $C10022, X
; STA $7B
; JML $C1001A


; WORKS FINE, this will instead trigger only on pause during battle

org $C116E6
JML BattleHook

org !ADDRESS_battlehook
BattleHook:
rep #$20
pha
lda !input
cmp #$2030 ; L R Select
BEQ BattleHookAnnihilate
BNE BattleHookFinish

; if condition met, set characters dead
BattleHookAnnihilate:
sep #$20
LDA #$40
sta $201A
sta $209A
sta $211A
sta $219A
rep #$20

; original code
BattleHookFinish:
pla
sep #$20
LDA #$01
STA $DB9A
CLC
JML $C116EC