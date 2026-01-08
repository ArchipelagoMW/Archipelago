hirom

org $C92424

db $A0, $01                     ;(Message) 01
db $70                          ;Very short pause
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $DE, $26				; set up reward
db $DF					; call text handler
db $E4, $CB                     ;Unknown
db $29                          ;Player pose: face up, right hand raised in
db $00                          ;Player Hold
db $CB, $2A, $00                ;Turn off bit 04 at address  0x7e0a59
db $CE, $0A, $02                ;Play next 02 bytes 0A times
db $B0, $64                     ;Subtract 64 Gil 
db $B4, $21                     ;Play Background Music Harvest
db $A2, $0C                     ;Turn on bit 10 at address 0x7e0a15
db $FF                          ;End Event

pad $C9243E