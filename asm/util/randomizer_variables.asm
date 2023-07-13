.gba

; This is the upper halfword of entry passage level 3.
; This level doesn't actually exist, so we can sneak this bit of extra save data
; in there.
.definelabel ReceivedItemCount, LevelStatusTable + 14  ; halfword

; Extends the existing box system to include full health boxes
.definelabel HasFullHealthItem, UnusedRamStart + 0  ; byte

; Items can be received one at a time w/o issue
.definelabel IncomingItemID, UnusedRamStart + 1  ; byte
.definelabel IncomingItemSender, UnusedRamStart + 2 ; 17 bytes

; The jewel piece or CD that you've most recently received or grabbed from a box
.definelabel LastCollectedItemID, UnusedRamStart + 19  ; byte
; Same values as "Has X" variables
.definelabel LastCollectedItemStatus, UnusedRamStart + 20  ; byte

.definelabel DeathlinkEnabled, UnusedRamStart + 21  ; byte

.definelabel QueuedJunk, UnusedRamStart + 24  ; bytes
    .definelabel QueuedFullHealthItem, QueuedJunk + 0
    .definelabel QueuedFormTraps, QueuedJunk + 1
    .definelabel QueuedHearts, QueuedJunk + 2
    .definelabel QueuedLightningTraps, QueuedJunk + 3

.definelabel Jewel1BoxContents, UnusedRamStart + 28  ; bytes
    .definelabel Jewel2BoxContents, Jewel1BoxContents + 1
    .definelabel Jewel3BoxContents, Jewel1BoxContents + 2
    .definelabel Jewel4BoxContents, Jewel1BoxContents + 3
    .definelabel CDBoxContents, Jewel1BoxContents + 4
    .definelabel HealthBoxContents, Jewel1BoxContents + 5

.definelabel Jewel1BoxExtData, Jewel1BoxContents + 8  ; words
    .definelabel Jewel2BoxExtData, Jewel1BoxExtData + 4
    .definelabel Jewel3BoxExtData, Jewel1BoxExtData + 8
    .definelabel Jewel4BoxExtData, Jewel1BoxExtData + 12
    .definelabel CDBoxExtData, Jewel1BoxExtData + 16
    .definelabel HealthBoxExtData, Jewel1BoxExtData + 20
