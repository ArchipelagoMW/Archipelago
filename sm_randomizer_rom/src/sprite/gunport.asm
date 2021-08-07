; --- rearrange dma gun port tables ---

; To break mirror symmetry, we will need to rearrange where the gun port tile
; data is held, and load it correctly during DMA. Thankfully, there's plenty of
; memory since Deerforce were very wasteful in this section.

; $90:C7A5 has pointers to the gun port DMA locations. The now free space at
; $90:86AF-87BC will be used for a table to DMA sets for all ten directions.

gun_port_dma = $9A9A00

org $9086AF

gun_port_table:

    !i = 0
    while !i < 10

    dw $0000
    dw gun_port_dma+(((0*10)+!i)*$20)
    dw gun_port_dma+(((1*10)+!i)*$20)
    dw gun_port_dma+(((2*10)+!i)*$20)

    !i #= !i+1
    endif

org $90C7A5

    dw gun_port_table+(0*8)
    dw gun_port_table+(1*8)
    dw gun_port_table+(2*8)
    dw gun_port_table+(3*8)
    dw gun_port_table+(4*8)
    dw gun_port_table+(5*8)
    dw gun_port_table+(6*8)
    dw gun_port_table+(7*8)
    dw gun_port_table+(8*8)
    dw gun_port_table+(9*8)


; --- reassign gun port tilemaps ---

; Gun ports are moved over to tile $DF which has alot of space since it is
; unused. We also remove the v/h flipping since the symmetry is broken up.

!gun_port_tile = $DF
!gun_port_flags = $28DF

org $90C786    ; DMA dest address based on tile number
    dw $6000+(!gun_port_tile*$10)

org $90C791    ; Set tilemap index and flags
    rep 10 : dw !gun_port_flags
