hirom

org $C9F733

db $DE, $28				; set up reward
db $DF					; call text handler
db $B4, $29                     ;Play Background Music Fanfare 1 (short)
db $39                          ;Player pose: face down, both arms raised
db $E4, $C9                     ;Unknown
db $48                          ;Player pose: garbage
db $0F                          ;<Unknown>
db $A4, $95                     ;Turn on bit 20 at address 0x7e0a46
db $FF                          ;End Event

pad $C9F741