hirom

; item prices unaffected, left at area $D12A00

; magic moved to F80000
; ability/crystals moved to F80200

org $C2F2BF
JML ReindexShop

org !ADDRESS_shopindexing
ReindexShop:

LDA $7E2802
CMP #$C0C0
BEQ ReindexAbilityShop

; if not ability, assume magic
LDA #$0000
LDA $F80000,x
STA $280A
JML $C2F2C6

ReindexAbilityShop:
LDA #$0000
LDA $F80200,x
STA $280A
JML $C2F2C6