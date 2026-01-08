from ..event.event import *

class Nikeah(Event):
    def name(self):
        return "Nikeah"

    def init_event_bits(self, space):
        space.write(
            field.SetEventBit(event_bit.BOARDED_CRIMSON_ROBBERS_BOAT_NIKEAH),
        )

    def mod(self):
        self.free_event_bit()
        self.airship_follow_boat_mod()

    def free_event_bit(self):
        # do not set event bit 0x2b0 so it can be used for other things
        space = Reserve(0xaed91, 0xaed92, "nikeah set event bit 0x2b0", field.NOP())

    def airship_follow_boat_mod(self):
        src = [
            vehicle.SetEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.LoadMap(0x01, direction.DOWN, default_music = False,
                            x = 147, y = 77, fade_in = False, airship = True),
            vehicle.SetPosition(147, 77),
            vehicle.ClearEventBit(event_bit.TEMP_SONG_OVERRIDE),
            vehicle.FadeLoadMap(0xbb, direction.DOWN, default_music = True,
                                x = 24, y = 11, fade_in = True, entrance_event = True),
            field.SetParentMap(0x01, direction.DOWN, x = 147, y = 76),
            field.Return(),
        ]
        space = Write(Bank.CA, src, "nikeah boat from south figaro move airship")
        move_airship = space.start_address

        space = Reserve(0xa932a, 0xa9336, "nikeah boat from south figaro load map", field.NOP())
        space.write(
            vehicle.Branch(move_airship),
        )
