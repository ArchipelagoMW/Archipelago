hirom
; this is for text clearing, it's constant and shouldnt be touched
org $E73568
pad $E736A0


; starts at index $60, at address $C0FB70
; torna canal key from zokk
org $C0FB70
db $30, $12





; FIXES TO CHANGES POINTERS TO KEY ITEMS:
; all of these below are specific bit setters based on the key item
; refer to chest_jobreward.asm for the code that calls these in
; at `BranchToKeyItemReward`

org !ADDRESS_keyitems

KeyItemTornaCanal:

LDA #$10
LDX #$0017
JSL SetKeyItemBits

LDA #$20
LDX #$0017
JSL SetKeyItemBits

RTL

KeyItemWalseKey:

LDA #$20
TRB $0A67

LDA #$01
LDX #$0068
JSL SetKeyItemBits


RTL

KeyItemSteamshipKey:
; blank for now, key item flag is enough

RTL

KeyItemIfritsFire:

LDA #$01
LDX #$0039
JSL SetKeyItemBits

LDA #$02
LDX #$0039
JSL SetKeyItemBits

; recently disabled for arch - seems bad to collect ifrits fire and despawn ifrit
; ifrit.asm should be despawning him as part of his event after fighting

; LDA #$80
; LDX #$0086
; JSL UnsetKeyItemBits

RTL

KeyItemSandWormBait:

LDA #$08
LDX #$001B
JSL SetKeyItemBits


RTL

KeyItemAdamantite:

LDA #$04
LDX #$0053
JSL SetKeyItemBits
LDA #$01
LDX #$00AF
JSL SetKeyItemBits


RTL


KeyItemBigBridge:
; blank for now, flag is enough

RTL

KeyItemMoogleSuit:

LDA #$10
LDX #$0039
JSL SetKeyItemBits

RTL


KeyItemSubmarineKey:

; write submarine coordinates if in world 2
LDA $000A2D
CMP #$02
BNE KeyItemSubmarineKeyFinish
lda #$30
sta $0AE9
lda #$00
sta $0AEA
lda #$AD
sta $0AEB
lda #$A5
sta $0AEC
KeyItemSubmarineKeyFinish:
RTL

KeyItemHiryuuCall:

; write hiryuu coordinates if in world 2
LDA $000A2D
CMP #$02
BNE KeyItemHiryuuCallFinish
lda #$2C
sta $0AE5
lda #$00
sta $0AE6
lda #$AC
sta $0AE7
lda #$A5
sta $0AE8
KeyItemHiryuuCallFinish:

RTL

KeyItemElderBranch:

LDA #$02
LDX #$0022
JSL SetKeyItemBits

RTL

KeyItemBracelet:
LDA #$20
LDX #$003C
JSL SetKeyItemBits

; reinstituted
; LDA #$20
; LDX #$0022
; JSL SetKeyItemBits

RTL

KeyItemAntiBarrier:

LDA #$40
TRB $0A1F

RTL

KeyItemPyramidPage:
RTL
KeyItemShrinePage:
RTL
KeyItemTrenchPage:
RTL
KeyItemFallsPage:
RTL

KeyItem1stTablet:
LDA #$08
LDX #$0024
JSL SetKeyItemBits
RTL
KeyItem2ndTablet:
LDA #$40
LDX #$0025
JSL SetKeyItemBits
RTL
KeyItem3rdTablet:
LDA #$02
LDX #$0026
JSL SetKeyItemBits
RTL
KeyItem4thTablet:
LDA #$08
LDX #$0026
JSL SetKeyItemBits
RTL


; this function will load in a bit address then set the correct bit 
; A = bit to set
; X = offset from $000A00
SetKeyItemBits:
ORA $0A00, x
STA $0A00, x

RTL

; Don't think this works correctly, use TRB method instead
UnsetKeyItemBits:
EOR $0A00, x
STA $0A00, x

RTL

