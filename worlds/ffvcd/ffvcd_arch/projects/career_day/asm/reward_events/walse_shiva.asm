hirom

org $C86F56

db $A0, $00                     ;(Message) 00
db $80, $0A                     ;Sprite 080 do event: Hide
db $BD, $05, $FF                ;Start Event Battle 05
db $70                          ;Very short pause
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $DE, $35				; set up reward
db $DF					; call text handler
db $C5, $80
db $B5, $02
db $71
db $DE, $84 ; custom reward
db $DF
db $E4, $B4                     ;Unknown
db $06                          ;Player Bounce in Place
db $CB, $D5, $00                ;Turn off bit 20 at address  0x7e0a6e
db $A2, $25                     ;Turn on bit 20 at address 0x7e0a18
db $FF                          ;End Event

pad $C86F6C