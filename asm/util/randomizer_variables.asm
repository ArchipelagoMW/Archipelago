.gba

; This is the upper halfword of entry passage level 3.
; This level doesn't actually exist, so we can sneak this bit of extra save data
; in there.
.definelabel ReceivedItemCount, LevelStatusTable + 14  ; halfword

; Extends the existing box system to include full health boxes
.definelabel HasFullHealthItem, UnusedRamStart + 0  ; byte

; Items can be received one at a time w/o issue
.definelabel IncomingItemID, UnusedRamStart + 1  ; byte
.definelabel IncomingItemSender, UnusedRamStart + 2  ; byte

; The jewel piece or CD that you've most recently received or grabbed from a box
.definelabel LastCollectedItemID, UnusedRamStart + 3  ; byte
; Same values as "Has X" variables
.definelabel LastCollectedItemStatus, UnusedRamStart + 4  ; byte

.definelabel DeathlinkEnabled, UnusedRamStart + 8  ; byte

.definelabel QueuedJunk, UnusedRamStart + 16  ; bytes
    .definelabel QueuedFullHealthItem, QueuedJunk + 0
    .definelabel QueuedFormTraps, QueuedJunk + 1
    .definelabel QueuedHearts, QueuedJunk + 2
    .definelabel QueuedLightningTraps, QueuedJunk + 3

.definelabel Jewel1BoxContents, UnusedRamStart + 24
.definelabel Jewel2BoxContents, UnusedRamStart + 26
.definelabel Jewel3BoxContents, UnusedRamStart + 28
.definelabel Jewel4BoxContents, UnusedRamStart + 30
.definelabel CDBoxContents, UnusedRamStart + 32
.definelabel HealthBoxContents, UnusedRamStart + 34
