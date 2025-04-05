from typing import Union, Iterable
from unittest import TestCase

from BaseClasses import MultiWorld
from ... import item_table, location_table
from ...mods.mod_data import ModNames


class ModAssertMixin(TestCase):
    def assert_stray_mod_items(self, chosen_mods: Union[Iterable[str], str], multiworld: MultiWorld):
        if isinstance(chosen_mods, str):
            chosen_mods = [chosen_mods]
        else:
            chosen_mods = list(chosen_mods)

        if ModNames.jasper in chosen_mods:
            # Jasper is a weird case because it shares NPC w/ SVE...
            chosen_mods.append(ModNames.sve)

        for multiworld_item in multiworld.get_items():
            item = item_table[multiworld_item.name]
            self.assertTrue(item.mod_name is None or item.mod_name in chosen_mods,
                            f"Item {item.name} has is from mod {item.mod_name}. Allowed mods are {chosen_mods}.")
        for multiworld_location in multiworld.get_locations():
            if multiworld_location.address is None:
                continue
            location = location_table[multiworld_location.name]
            self.assertTrue(location.mod_name is None or location.mod_name in chosen_mods)
