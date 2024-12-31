"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the energy form and dual form (and Li)
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import EarlyEnergyForm, TurtleRandomizer


class EnergyFormDualFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the energy form and dual form (and Li)"""
    options = {
        "early_energy_form": EarlyEnergyForm.option_off,
        "turtle_randomizer": TurtleRandomizer.option_all
    }

    def test_energy_form_or_dual_form_location(self) -> None:
        """Test locations that require Energy form or dual form"""
        locations = [
            AquariaLocationNames.NAIJA_S_HOME_BULB_AFTER_THE_ENERGY_DOOR,
            AquariaLocationNames.HOME_WATERS_NAUTILUS_EGG,
            AquariaLocationNames.ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK,
            AquariaLocationNames.ENERGY_TEMPLE_BOTTOM_ENTRANCE_KROTITE_ARMOR,
            AquariaLocationNames.ENERGY_TEMPLE_THIRD_AREA_BULB_IN_THE_BOTTOM_PATH,
            AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG,
            AquariaLocationNames.ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
            AquariaLocationNames.MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG,
            AquariaLocationNames.KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD,
            AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD,
            AquariaLocationNames.KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY,
            AquariaLocationNames.KING_JELLYFISH_CAVE_JELLYFISH_COSTUME,
            AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
            AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_IN_THE_LEFT_BOTTOM_ROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_IN_THE_LITTLE_PIPE_ROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_BEFORE_THE_BEDROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.THE_BODY_CENTER_AREA_BREAKING_LI_S_CAGE,
            AquariaLocationNames.THE_BODY_CENTER_AREA_BULB_ON_THE_MAIN_PATH_BLOCKING_TUBE,
            AquariaLocationNames.THE_BODY_LEFT_AREA_FIRST_BULB_IN_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_SECOND_BULB_IN_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_BELOW_THE_WATER_STREAM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM,
            AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_BOTTOM_FACE_ROOM,
            AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_JELLY_ZAP_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_NAUTILUS_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME,
            AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
            AquariaLocationNames.BEATING_FALLEN_GOD,
            AquariaLocationNames.BEATING_BLASTER_PEG_PRIME,
            AquariaLocationNames.BEATING_MITHALAN_GOD,
            AquariaLocationNames.BEATING_DRUNIAN_GOD,
            AquariaLocationNames.BEATING_LUMEREAN_GOD,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.BEATING_NAUTILUS_PRIME,
            AquariaLocationNames.BEATING_MERGOG,
            AquariaLocationNames.BEATING_MITHALAN_PRIESTS,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.BEATING_KING_JELLYFISH_GOD_PRIME,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.SUNKEN_CITY_CLEARED,
            AquariaLocationNames.FIRST_SECRET,
            AquariaLocationNames.OBJECTIVE_COMPLETE
        ]
        items = [[ItemNames.ENERGY_FORM, ItemNames.DUAL_FORM, ItemNames.LI_AND_LI_SONG, ItemNames.BODY_TONGUE_CLEARED]]
        self.assertAccessDependency(locations, items)
