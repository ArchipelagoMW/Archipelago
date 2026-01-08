hirom

;This is a new data table used by the progressive ability system
;Each entry is 8 bytes long and corresponds to a list of up to 8 progressive abitliies
;Abilities have a new form of reindexing, specific to chest rewards.
;The master list for a human readable form of this data is in utilities/tables/ability_progression.csv
;(I'm not going to comment the lines here, in case they change. Assume this file is up to date with the csv)

org $F80600
db $06, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $07, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $08, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $09, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $0A, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $0B, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $0C, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $0D, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $0E, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $0F, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $10, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $11, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $12, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $13, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $14, $15, $16, $FF, $FF, $FF, $FF, $FF
db $17, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $18, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $19, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $1A, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $1B, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $1C, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $1D, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $1E, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $1F, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $20, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $21, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $22, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $24, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $27, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $28, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $29, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $2A, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $30, $31, $32, $33, $34, $35, $FF, $FF
db $38, $39, $3A, $3B, $3C, $3D, $FF, $FF
db $40, $41, $42, $43, $44, $45, $FF, $FF
db $48, $49, $4A, $4B, $4C, $4D, $FF, $FF
db $50, $51, $52, $53, $54, $FF, $FF, $FF
db $58, $59, $5A, $60, $FF, $FF, $FF, $FF
db $61, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $68, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $69, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $6A, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $6B, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $6C, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $6D, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $6E, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $6F, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $70, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $71, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $72, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $73, $74, $75, $FF, $FF, $FF, $FF, $FF
db $76, $77, $FF, $FF, $FF, $FF, $FF, $FF
db $78, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $79, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $7A, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $7B, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $7C, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $7D, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $7E, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $7F, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $80, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $81, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $82, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $83, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $84, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $85, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $86, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $87, $FF, $FF, $FF, $FF, $FF, $FF, $FF
db $88, $FF, $FF, $FF, $FF, $FF, $FF, $FF