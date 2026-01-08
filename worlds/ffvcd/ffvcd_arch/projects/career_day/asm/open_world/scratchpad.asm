hirom
; used for testing misc hacks until they go into their own file


; beginner's hut chests

; MAGIC
org $D13216
db $20, $01
org $D1321A
db $20, $01
org $D1321E
db $20, $01
org $D13222
db $20, $01

; ABILITIES
org $D13216
db $60, $20
org $D1321A
db $60, $20
org $D1321E
db $60, $20
org $D13222
db $60, $20

; ; KEY ITEMS
; org $D13216
; db $30, $00
; org $D1321A
; db $30, $01
; org $D1321E
; db $30, $02
; org $D13222
; db $30, $03



; wind crystal

; magic
org $C0FAB2
db $20, $01, $20, $01, $20, $01, $20, $01

; abilities
org $C0FAB2
db $60, $20, $60, $20, $60, $20, $60, $20

