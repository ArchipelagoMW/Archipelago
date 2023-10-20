.gba

; Object tiles in VRAM
.definelabel TilesReceived8, 0x06012180
.definelabel TilesFrom4, 0x06012280
.definelabel TilesSenderA8, 0x06012600
.definelabel TilesSenderB8, 0x06012A00
.definelabel TilesItemA12, 0x06012180
.definelabel TilesItemB8, 0x06012600
.definelabel TilesItemC8, 0x06012A00

; These extra bits of save data are stored in the upper parts of Entry Passage
; levels that don't exist.
; Most significant byte of the "third" level
.definelabel WarioAbilities, LevelStatusTable + 11
; Upper halfword of the "fourth" level
.definelabel ReceivedItemCount, LevelStatusTable + 14

; Extends the existing box system to include full health boxes
.definelabel HasFullHealthItem, UnusedRamStart + 0  ; byte

; Items can be received one at a time w/o issue
.definelabel IncomingItemID, UnusedRamStart + 1  ; byte

; 0 = Nothing
; 1 = Just received item
; 2 = Displaying text after receiving item
; 3 = Displaying text after collecting someone else's item
.definelabel MultiworldState, UnusedRamStart + 2  ; byte

.definelabel IncomingItemSender, UnusedRamStart + 3 ; 17 bytes

; The jewel piece or CD that you've most recently received or grabbed from a box
.definelabel LastCollectedItemID, UnusedRamStart + 20  ; byte
; Same values as "Has X" variables
.definelabel LastCollectedItemStatus, UnusedRamStart + 21  ; byte

.definelabel DeathlinkEnabled, UnusedRamStart + 22  ; byte

.definelabel TextTimer, UnusedRamStart + 23  ; byte

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

; Indicates which icon is next to be selected and changed when a box is opened
; with treasure in it. Loops around four values, values of upper six bits
; unspecified and ignored.
.definelabel CurrentJewelIconPosition, HealthBoxExtData + 4  ; byte

; Tracks what abilities you've found in this level but haven't properly
; collected yet.
.definelabel AbilitiesInThisLevel, HealthBoxExtData + 5  ; byte
