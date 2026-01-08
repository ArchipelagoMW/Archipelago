hirom

; Allows pivot on ability shop
org $C0F1F3
db $C0 

; Always allow sell to appear
; nop ASM command out a bit test / branch if minus
org $c2f17b
nop
nop
nop
nop
nop

; allow magic to sell 
org $c2aad6
bra $aae8

; allow all shops to increase inv count
org $c2a618
jmp $a61e


org $C2F12B
JML ShopHook


org !ADDRESS_shophook
ShopHook:
TXY
PHA
LDA $7E2802
CMP #$0000
BEQ JumpToItemShop
CMP #$8080
BEQ JumpToMagicShop
CMP #$C0C0
BEQ JumpToAbilityShop
BNE JumpToItemShop

JumpToItemShop:
PLA
JML $C2F131
JumpToMagicShop:
PLA
JML $C2F136

JumpToAbilityShop:
PLA
STA $7E2802 ; temporarily store here for addition, going to repopulate with $C0C0 later

; janky stack manip
LDA #$F133
PHA

LDA $7E2802 
php 
rep #$20
and #$00FF
pha
LDA #$9A00
STA $7E2802 ; temporarily store here for addition, going to repopulate with $C0C0 later
pla
asl a
asl a
asl a
CLC
ADC $7E2802
tyx
tay

LDA #$C0C0 ; restore ability crystal type
STA $7E2802

lda #$E708 ; set up to data bank $E7, $08 text limit
JML $C2E449 ; original code resume, hopefully preserving stack















; This code checks if the player already has the ability or reward

org $C2F05B
JML CheckShopRewardInInventory

org !ADDRESS_shopcheckreward
CheckShopRewardInInventory:
SEP #$20
PHA 
LDA $7E2802
CMP #$C0
BEQ CheckAbilityOrCrystal
BNE CheckMagicReward ; if magic shop, check magic



CheckMagicReward:
PLA
AND $0950,x
BEQ RewardCheckPass
; if reward already in inventory, do not award it 
BNE RewardCheckFail

RewardCheckFail:
JML $C2F062

; if reward not in inventory, award it
RewardCheckPass:
JML $C2F065


CheckAbilityOrCrystal:

; We're in an ability/crystal shop but need to know if its one or the other
; $88 is the final index for abilities, then switches to crystals at $89
; Check if greater than $89, if so, then reduce by $89 and move on to
; award a job. Else award an ability


CLC
LDA $7E2809 ; current reward ID
CMP #$89
BCS BranchAwardCrystal
JMP CheckAbilityRewardChar1

BranchAwardCrystal:
JML CheckAwardCrystal



CheckAbilityRewardChar1:
PLA
STA $7E2802 ; use this address temporarily

AND $08F7,x
BEQ RewardAbilityCheckPass
BNE CheckAbilityRewardChar2

CheckAbilityRewardChar2:
LDA $7E2802
AND $090B,x
BEQ RewardAbilityCheckPass
BNE CheckAbilityRewardChar3

CheckAbilityRewardChar3:
LDA $7E2802
AND $091F,x
BEQ RewardAbilityCheckPass
BNE CheckAbilityRewardChar4

CheckAbilityRewardChar4:
LDA $7E2802
AND $0933,x
BEQ RewardAbilityCheckPass
BNE RewardAbilityCheckFail

RewardAbilityCheckFail:
LDA #$C0
STA $7E2802
JML $C2F062

; if reward not in inventory, award it
RewardAbilityCheckPass:
LDA #$C0
STA $7E2802
JML $C2F065



CheckAwardCrystal:
PLA
ASL 
; if 00, needs to be 01 for next
BEQ SetAwardCrystal2
BNE FinalizeAwardCrystal2

SetAwardCrystal2:
dex
LDA #$01

FinalizeAwardCrystal2:
; take contents of A (the newly asl'd bit to check)
AND $00082F,x
BEQ RewardAbilityCheckPass
BNE RewardAbilityCheckFail

















; This code awards the player's crystal/ability inventory
org $C2F012
JML !ADDRESS_shopawardreward

org !ADDRESS_shopawardreward
PHA
LDA $7E2802
CMP #$C0
BEQ CheckAbilityCrystalShopID

; DefaultMagicShop 
PLA
ora $000950,x
sta $000950,x
JML $C2F01A





CheckAbilityCrystalShopID:
; Check crystal or ability. Crystal >= $89 
CLC
LDA $7E2809 ; current reward ID
CMP #$89
BCS BranchRewardCrystal
; Branches if crystal, otherwise treat as ability
JML AwardShopAbility

BranchRewardCrystal:
JML AwardCrystal

AwardShopAbility:
PLA

; temporarily use this address for storing what bit to affect
STA $7E2802

; first check who needs to increase their ability count

; Char1
LDA $0008F7,x
AND $7E2802
BEQ AwardAbilityCountChar1
BNE AwardAbilityCountStartChar2
AwardAbilityCountChar1: 
inc !1pabilitiescount

AwardAbilityCountStartChar2:


LDA $00090B,x
AND $7E2802
BEQ AwardAbilityCountChar2
BNE AwardAbilityCountStartChar3
AwardAbilityCountChar2: 
inc !2pabilitiescount

AwardAbilityCountStartChar3:


LDA $00091F,x
AND $7E2802
BEQ AwardAbilityCountChar3
BNE AwardAbilityCountStartChar4
AwardAbilityCountChar3: 
inc !3pabilitiescount

AwardAbilityCountStartChar4:


LDA $000933,x
AND $7E2802
BEQ AwardAbilityCountChar4
BNE FinishedCheckingAbilityCounts
AwardAbilityCountChar4: 
inc !4pabilitiescount


FinishedCheckingAbilityCounts:

; push into stack 3 times...?
LDA $7E2802

PHA
PHA
PHA

; Char1
ora $0008F7,x
sta $0008F7,x
; Char2
PLA
ora $00090B,x
sta $00090B,x
; Char3
PLA
ora $00091F,x
sta $00091F,x
PLA
; Char4
ora $000933,x
sta $000933,x

LDA #$C0
STA $7E2802


JML $C2F01A



AwardCrystal:
PLA
ASL 
; if 00, needs to be 01 for next
BEQ SetAwardCrystal
BNE FinalizeAwardCrystal

SetAwardCrystal:
dex
LDA #$01

FinalizeAwardCrystal:

ora $00082F,x
sta $00082F,x
JML $C2F01A








; This code hooks into where magic is checked to see if there's a magicsword equivalent and 
; award it to the player
; We want to disable entirely for abilities and jobs 

if !vanillarewards = 0
    org $C2EFF0
    JML CheckMagicSwordAward


    org !ADDRESS_shopmagicsword
    CheckMagicSwordAward:
    PHA
    LDA $7E2802
    CMP #$89
    BEQ HandleMagicSword
    BNE SkipMagicSword

    ; if it's magic still, replicate magic sword checking then jump back
    HandleMagicSword:

    PLA
    LDX $8E
    MagicSwordStart:
    LDA $D12890,x
    BEQ MagicSwordAward1
    CMP $2809
    BEQ MagicSwordAward2
    inx
    inx
    BRA MagicSwordStart

    MagicSwordAward1:
    JML $C2F008
    MagicSwordAward2:
    JML $C2F001


    SkipMagicSword:
    PLA
    JML $C2F008
endif