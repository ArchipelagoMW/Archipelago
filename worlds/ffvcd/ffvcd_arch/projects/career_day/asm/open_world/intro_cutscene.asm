hirom


; $C84C80 → $C84FD0
; Intro cutscene skips
; Apparently, the first two lines spawn the Tycoon meteor, but another event doesn't appear to be called. Unsure atm 

org $C84C80

db $7A                          ;Naming Character

; all flags related to setting up open world are in this file
incsrc ../open_world/starting_flags.asm

;db $E1, $10, $00, $91, $1C, $00 ;Return from cutscene? 10 00 91 1C 00
db $A4, $E0                     ;Turn on bit 01 at address 0x7e0a50


; db $B1, $05                     ;Set Player Sprite 07 (Faris ;])
db $09                          ;Player Show
; db $02                          ;Player Move Right
db $C6, $12                     ;Add job Bard
db $AA, $E0                     ;Add Item Potion
db $AA, $E0                     ;Add Item Potion
db $AA, $E0                     ;Add Item Potion
db $CB, $58, $00	            ;Clear Flag 2/3/4/5/58 00 ;removes faris sleeping in tule
; db $A4, $DC                     ;Set Event Flag 1DC ; DISABLED in v0.75, appears to only be tied to 4 crystal barriers on world map in world 1. MOVED TO WIND SHRINE
; db $A4, $FF                     ;Set Event Flag 1FF *this ordinarily disables enka*
db $EE                          ;Conditional event flag checks for world 1 (mostly Ronka access)

db $C3, $02                     ;Fade in Speed 08
db $D2, $00, $B9, $86, $D8
db $E1, $00, $00, $B8, $85, $00 ;Return from cutscene? 00 00 9C 96 00


; OG CORRECT WARPS
db $75                          ;Long pause
db $EC                          ;Set starting randomizer job

; TESTING!!!!
; db $B4, $22                     ; CUSTOM MUSIC
; db $75
; db $75
; db $75
; db $B4, $36                     ; CUSTOM MUSIC

if !starting_cara = 1
    db $B7, $8A							;Add/Remove character 02 (Galuf)
    db $B7, $0C							;Add/Remove character 02 (Galuf)
endif

db $FF                          ;End Event

padbyte $00
pad $C84FD0