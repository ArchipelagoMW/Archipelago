hirom

;This is a new data table used by the progressive magic system
;Each entry is 4 bytes long and corresponds to a list of up to 4 progressive magic spells
;Spells have a new form of reindexing, specific to chest rewards.
;The master list for a human readable form of this data is in utilities/tables/magic_progression.csv
;(I'm not going to comment the lines here, in case they change. Assume this file is up to date with the csv)

org $F80400
db $00, $06, $0C, $FF
db $01, $07, $0D, $FF
db $02, $08, $0E, $FF
db $03, $09, $0A, $FF
db $04, $11, $0F, $FF
db $05, $0B, $10, $FF
db $12, $18, $1E, $FF
db $16, $1C, $1F, $23
db $15, $17, $20, $FF
db $14, $1B, $1D, $FF
db $13, $1A, $22, $FF
db $19, $21, $FF, $FF
db $24, $2A, $30, $FF
db $25, $2B, $31, $FF
db $26, $2C, $32, $FF
db $27, $2D, $2E, $FF
db $28, $35, $34, $FF
db $29, $2F, $33, $FF
db $37, $3D, $40, $FF
db $38, $3B, $41, $47
db $39, $3C, $42, $44
db $3A, $3E, $43, $46
db $3F, $45, $FF, $FF
db $48, $4E, $4F, $53
db $49, $51, $54, $52
db $4A, $50, $55, $FF
db $4B, $4C, $4D, $56
db $57, $59, $FF, $FF
db $58, $5C, $FF, $FF
db $5A, $5D, $FF, $FF
db $5E, $5B, $FF, $FF
db $86, $88, $87, $85
db $8F, $90, $91, $FF
db $89, $8A, $8D, $FF
db $82, $83, $94, $84
db $95, $9A, $FF, $FF
db $8B, $8C, $99, $8E
db $9C, $96, $9B, $FF
db $93, $92, $9F, $9D
db $98, $97, $9E, $FF