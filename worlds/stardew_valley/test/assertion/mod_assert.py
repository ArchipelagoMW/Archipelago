from typing import Iterable
from unittest import TestCase

from BaseClasses import MultiWorld
from ... import item_table, location_table
from ...content.content_packs import vanilla_content_pack_names
from ...mods.mod_data import ModNames


class ModAssertMixin(TestCase):
    def assert_stray_mod_items(self, chosen_content_packs: Iterable[str] | str, multiworld: MultiWorld):
        if isinstance(chosen_content_packs, str):
            chosen_content_packs = vanilla_content_pack_names | {chosen_content_packs}
        else:
            chosen_content_packs = vanilla_content_pack_names | set(chosen_content_packs)

        if ModNames.jasper in chosen_content_packs:
            # Jasper is a weird case because it shares NPC w/ SVE...
            chosen_content_packs |= {ModNames.sve}

        for multiworld_item in multiworld.get_items():
            item = item_table[multiworld_item.name]
            self.assertTrue(item.content_packs.issubset(chosen_content_packs),
                            f"Item {item.name} requires content packs {item.content_packs}. Allowed mods are {chosen_content_packs}.")
        for multiworld_location in multiworld.get_locations():
            if multiworld_location.address is None:
                continue
            location = location_table[multiworld_location.name]
            self.assertTrue(location.content_packs.issubset(chosen_content_packs),
                            f"Location {location.name} requires content packs {location.content_packs}. Allowed mods are {chosen_content_packs}.")
