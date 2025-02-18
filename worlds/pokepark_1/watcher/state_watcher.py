import traceback

from worlds.pokepark_1 import REGION_UNLOCK
from worlds.pokepark_1.adresses import green_zone_trigger_address, green_zone_states_word, green_zone_trigger_value, \
    green_zone_keep_state, green_zone_states_byte, beach_zone_trigger_address, beach_zone_trigger_value, \
    beach_zone_states_hword, beach_zone_states_byte, beach_zone_states_word, region_unlock_item_checks
import dolphin_memory_engine as dme
import asyncio
from CommonClient  import logger

delay_seconds = 1


class StateSetup:
    # trigger_address_byte_range 4= word(4), 2= hword(2), 1 = byte (1)
     def __init__(self, trigger_address, trigger_address_byte_range, trigger_state, changes_word, changes_hword, changes_byte):
         self.trigger_address = trigger_address
         self.address_range = trigger_address_byte_range
         self.trigger_state = trigger_state
         self.changes_word = changes_word
         self.changes_byte = changes_byte
         self.changes_hword = changes_hword
         self.executed = False

     def process(self):
         if self.address_range == 2:
            current_state = int.from_bytes(dme.read_bytes(self.trigger_address, 2), byteorder='big')
         elif self.address_range == 4:
             current_state = dme.read_word(self.trigger_address)
         elif self.address_range == 1:
             current_state = dme.read_byte(self.trigger_address)
         else:
             return

         if not self.executed and current_state == self.trigger_state:
             for address, value in self.changes_word:
                 dme.write_word(address, value)
             for address, value in self.changes_byte:
                 dme.write_byte(address, value)
             for address, value in self.changes_hword:
                 dme.write_bytes(address, value.to_bytes(2, byteorder='big'))
             self.executed = True

class ZoneStateManager:
    def __init__(self):
        self.current_zone = "meadow"
        self.fast_travel_address = 0x8037502F
        self.activate_fast_travel = {
            "meadow": 0x80,
            "beach": 0x40
        }
        self.active_zones = {"meadow"}

        self.states = {
            "meadow": StateSetup(
                green_zone_trigger_address,
                4,
                green_zone_trigger_value,
                green_zone_states_word,
                [],
                green_zone_states_byte
            ),
            "beach": StateSetup(
                beach_zone_trigger_address,
                2,
                beach_zone_trigger_value,
                beach_zone_states_word,
                beach_zone_states_hword,
                beach_zone_states_byte
            )
        }
        self.keep_states = {
            "meadow": green_zone_keep_state,
            "beach": []
        }

    def check_zone_transition(self, ctx):
        if REGION_UNLOCK.get("Beach Zone Unlock") in [item.item for item in ctx.items_received]:
            self.current_zone = "beach"
            self.active_zones.add("beach")

            if not self.states["beach"].executed:
                for address, value in region_unlock_item_checks[REGION_UNLOCK.get("Beach Zone Unlock")]:
                    dme.write_bytes(address, value.to_bytes(2, byteorder='big'))

    def process(self):
        self.states[self.current_zone].process()

        total_value = sum(self.activate_fast_travel[zone] for zone in self.active_zones)
        dme.write_byte(self.fast_travel_address, total_value)

        for address, expected_value in self.keep_states[self.current_zone]:
            if dme.read_byte(address) == expected_value:
                dme.write_byte(address, expected_value)


zone_manager = ZoneStateManager()


async def state_watcher(ctx):
    def _sub():
        if not dme.is_hooked():
            return

        zone_manager.check_zone_transition(ctx)
        zone_manager.process()

    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked():
                dme.hook()
            else:
                _sub()
        except Exception as e:
            logger.error(f"Error in location_state_watcher: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            raise
        await asyncio.sleep(delay_seconds)


