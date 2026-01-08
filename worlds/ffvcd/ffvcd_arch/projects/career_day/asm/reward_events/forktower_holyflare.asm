hirom

org $c9a22f

; db $A4, $FE                     ;Turn on bit 40 at address 0x7e0a53
;db $71                          ;Short pause
db $C8, $35, $07                ;Display Message/Text/Dialogue 35 07
;db $71                          ;Short pause
; db $16                          ;Player pose: face left, standing
; ;db $73                          ;Long pause
; db $E3, $9A, $01, $1F, $08, $00 ;Inter-map cutscene? 9A 01 1F 08 00
; db $0A                          ;Player Hide
; db $C3, $0C                     ;Fade in Speed 0C
; db $73                          ;Long pause
; db $C8, $36, $07                ;Display Message/Text/Dialogue 36 07
; db $71                          ;Short pause
; db $77                          ;<Unknown>
; db $CE, $10, $01                ;Play next 01 bytes 10 times
; db $04                          ;Player move Left
; ;db $71                          ;Short pause
; db $C8, $37, $07                ;Display Message/Text/Dialogue 37 07
; ;db $71                          ;Short pause
; db $CE, $10, $01                ;Play next 01 bytes 10 times
; db $02                          ;Player Move Right
; db $A5, $FE                     ;Turn off bit 40 at address 0x7e0a53
; db $E3, $9D, $01, $2D, $23, $00 ;Inter-map cutscene? 9D 01 2D 23 00
; db $09                          ;Player Show
; db $76                          ;<Unknown>
; db $C3, $0C                     ;Fade in Speed 0C
db $71
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $0A                     ;Sprite 080 do event: Hide
db $BD, $30, $FF                ;Start Event Battle 30
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $39                          ;Player pose: face down, both arms raised
db $DE, $1F				; set up reward
db $DF					; call text handler
db $C5, $80
db $B5, $02
db $71
db $DE, $7D ; custom reward
db $DF

db $E4, $E3                     ;Unknown
db $93, $01                     ;Sprite 193 do event: Move Up
db $2D                          ;Player pose: face right, right hand out
db $22                          ;Player pose: face down, left hand on head
db $71
db $00                          ;Player Hold
db $FF                          ;End Event

; pad $C9A27C
org $C84364
db $50, $A5, $C9
org $C9A550


db $7C                          ;<Unknown>
; db $10                          ;Player pose: face up, left hand forward
; db $71                          ;Short pause
db $80, $03                     ;Sprite 080 do event: Move Down
db $80, $0A                     ;Sprite 080 do event: Hide
; db $70                          ;Very short pause
db $BD, $2F, $FF                ;Start Event Battle 2F


; turn on so arch can see boss defeated flag
db $A4, $F2                     ;Turn on bit 04 at address 0x7e0a52 - this would ordinarily cause world map to change
db $72

db $B4, $29                     ;Play Background Music Fanfare 1 (short)
; db $39                          ;Player pose: face down, both arms raised
; db $C5, $20                     ;<unknown>
; db $71                          ;Short pause
db $DE, $20				; set up reward
db $DF					; call text handler
db $C5, $80
db $B5, $02
db $71
db $DE, $7E ; custom reward
db $DF
db $E4, $14                     ;Unknown
; db $B9, $63                     ;Toggle Subtracitve Tint by 63
; db $B3, $10                     ;Pause for 100 cycles
; db $12                          ;Player pose: face right, standing
; db $16                          ;Player pose: face left, standing
; db $12                          ;Player pose: face right, standing
; db $16                          ;Player pose: face left, standing
; db $14                          ;Player pose: face down, left hand forward
; db $C8, $3A, $07                ;Display Message/Text/Dialogue 3A 07
db $C4, $03                     ;Fade out Speed 02
db $73

; arch - do not change tiles on world map, allowing fork tower to be re-done
db $A5, $F2                     ;Turn on bit 04 at address 0x7e0a52 - this would ordinarily cause world map to change

; these are fork tower flags for "in fork tower mode" that will get set off after finishing
db $A5, $70            ; set address 000A42 bit OFF 01
db $A5, $60            ; set address 000A40 bit OFF 01
db $A5, $61            ; set address 000A40 bit OFF 02
db $A5, $62            ; set address 000A40 bit OFF 04
db $A5, $63            ; set address 000A40 bit OFF 08
db $A5, $56            ; set address 000A3E bit OFF 40
db $A5, $57            ; set address 000A3E bit OFF 80
db $A5, $58            ; set address 000A3F bit OFF 01
db $A5, $59            ; set address 000A3F bit OFF 02
db $A5, $5A            ; set address 000A3F bit OFF 04
db $A5, $5B            ; set address 000A3F bit OFF 08
db $A5, $5C            ; set address 000A3F bit OFF 10
db $A5, $5D            ; set address 000A3F bit OFF 20
db $A5, $5E            ; set address 000A3F bit OFF 40
db $A5, $5F            ; set address 000A3F bit OFF 80
db $A5, $6F

db $E1, $02, $00, $CE, $CA, $00 ;Return from cutscene? 02 00 CE CA 00
db $B7, $00                     ;Add/Remove character 00
db $B7, $09                     ;Add/Remove character 09
db $B7, $0B                     ;Add/Remove character 0B
db $B7, $0C                     ;Add/Remove character 0C
db $7D                          ;<Unknown>
db $14                          ;Player pose: face down, left hand forward
db $DB                          ;Restore Player status
db $C3, $03                     ;Fade in Speed 02
db $73
db $FF                          ;End Event

pad $C9A2CB