from ..memory.space import Reserve

class WorldMap:
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

    def world_minimap_high_contrast_mod(self):
        # Thanks to Osteoclave for identifying these changes

        # Increases the sprite priority for the minimap sprites
        # So it gets drawn on top of the overworld instead of being translucent
        #ee4146=1b
        space = Reserve(0x2e4146, 0x2e4146, "minimap sprite priority")
        space.write(0x1b) # default: 0x0b

        # Colors bytes: gggrrrrr, xbbbbbgg
        # High contrast location indicator on minimaps
        # d2eeb8=ff + d2eeb9=7f
        # d2efb8=ff + d2efb9=7f
        location_indicator_addr = [0x12eeb8,  # WoB default: 1100
                                   0x12efb8]  # WoR default: 1100
        for loc_addr in location_indicator_addr:
            space = Reserve(loc_addr, loc_addr+1, "high contrast minimap indicator")
            space.write(0xff, 0x7f)

        # d2eeba=ff + d2eebb=7f
        # d2efba=ff + d2efbb=7f
        location_indicator_addr = [0x12eeba,  # WoB default: 1f00
                                   0x12efba]  # WoR default: 1f00
        for loc_addr in location_indicator_addr:
            space = Reserve(loc_addr, loc_addr+1, "high contrast minimap indicator")
            space.write(0xff, 0x7f) 

        # Additional minimap palette mods
        # default: 84 10 e7 1c 4a 29 10 42 ff 7f
        # WoB: d2eea2=00 + d2eea3=14 + d2eea4=82 + d2eea5=28 + d2eea6=e4 + d2eea7=38 + d2eea8=67 + d2eea9=51 + d2eeaa=9c + d2eeab=02
        # WoR: d2efa2=00 + d2efa3=14 + d2efa4=82 + d2efa5=28 + d2efa6=e4 + d2efa7=38 + d2efa8=67 + d2efa9=51 + d2efaa=9c + d2efab=02
        minimap_palette_bytes = [0x00, 0x14, 0x82, 0x28, 0xe4, 0x38, 0x67, 0x51, 0x9c, 0x02]
        minimap_palette_addr = [0x12eea2, # WoB
                                0x12efa2] # WoR
        for addr in minimap_palette_addr:
            space = Reserve(addr, addr+len(minimap_palette_bytes)-1, "minimap palette")
            space.write(minimap_palette_bytes)

        # This changes the color of the Floating Continent (pre-floating) on WoB
        # default: e7 1c 4a 29 10 42
        # d2eeac=82 + d2eead=28 + d2eeae=e4 + d2eeaf=38 + d2eeb0=67 + d2eeb1=51
        addr = 0x12eeac
        minimap_palette_bytes = [0x82, 0x28, 0xe4, 0x38, 0x67, 0x51]
        space = Reserve(addr, addr+len(minimap_palette_bytes)-1, "floating continent palette")
        space.write(minimap_palette_bytes)

    def mod(self):
        if self.args.world_minimap_high_contrast:
            self.world_minimap_high_contrast_mod()