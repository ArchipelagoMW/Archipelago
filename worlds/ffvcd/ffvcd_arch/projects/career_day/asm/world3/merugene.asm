hirom


; $C8AA8E → $C8AD90

org $C8AA8E





db $B5, $5D                     ;Play Sound Effect Dragon cry

db $D3, $87, $13, $1E           ;Sprite 80 set map position 13, 1E
db $D3, $85, $13, $1F           ;Sprite 81 set map position 13, 18
db $87, $09
db $87, $2F
db $85, $09
db $85, $42


db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $03                          ;Player Move Down
db $03                          ;Player Move Down
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $02                          ;Player Move Right
db $03                          ;Player Move Down
db $73
; db $A4, $F6                     ;Set Event Flag 1F6
; db $A5, $FE                     ;Clear Event Flag 1FE


db $87, $0A
db $BD, $2B, $FF                ;Start Event Battle 2B
db $C5, $80
db $B5, $02
db $71
db $DE, $7A ; custom reward
db $DF
db $71
db $03
; db $D2, $02, $57, $69, $D5      ;(Map) 02 57 69 D5

db $C4, $02
db $75

db $E1, $02, $00, $39, $79, $00 ;Return from cutscene? 02 00 39 79 00
db $DB                          ;Restore Player status
db $09                          ;Player Show
db $02                          ;Player Move Right
db $C3, $02                     ;Fade in Speed 08
db $73                          ;Long pause
; CAREERDAY
; db $A2, $81                     ;Set Event Flag 081
; db $CA, $99, $03                ;Set Flag 2/3/4/5/99 03
; db $CA, $5D, $02                ;Set Flag 2/3/4/5/5D 02
; db $CA, $5E, $02                ;Set Flag 2/3/4/5/5E 02
; db $CA, $0C, $00                ;Set Flag 2/3/4/5/0C 00
; db $A4, $9B            ; set address 000A47 bit ON 08. THIS WAS REPURPOSED FOR EXDEATH WORLD 2
; db $B7, $09                     ;Add/Remove character 09
; db $A8, $7F                     ;Adjust Character HP by 7F
; db $BB, $01, $80                ;Set Character Lenna  Curable status to Wounded
db $FF                          ;End Event


padbyte $00
pad $C8AD90