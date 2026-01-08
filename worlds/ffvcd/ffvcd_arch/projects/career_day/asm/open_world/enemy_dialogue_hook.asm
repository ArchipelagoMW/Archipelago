hirom

; hooking into an arbitrary place in the dialogue code in battle
; if a certain condition is met, set event flag, otherwise move on


; org $c23cae
; JML $F00B20

; org $F00B20
; phx
; pha

; rep #$20
; ; this is saying if youre in the portal cave, then update event flag
; lda !mapid
; CMP #$0121
; BNE BattleDialogueOriginalCode
; lda !xycoordcheck
; CMP #$0A08
; BNE BattleDialogueOriginalCode

; ; if both met, then manually change event flag
; sep #$20
; LDA #$02
; TSB $0A49


; BattleDialogueOriginalCode: 
; sep #$20
; pla
; plx

; lda $4367,x
; sta $46d6,y
; inx
; iny


; jml $c23cb6
