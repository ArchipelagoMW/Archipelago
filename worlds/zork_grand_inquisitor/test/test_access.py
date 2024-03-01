from typing import List

from . import ZorkGrandInquisitorTestBase

from ..enums import (
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
)


class AccessTestRegions(ZorkGrandInquisitorTestBase):
    options = {
        "start_with_hotspot_items": "false",
    }

    def test_access_crossroads_to_dm_lair_sword(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_crossroads_to_dm_lair_teleporter(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_crossroads_to_gue_tech(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_REZROV.value,
                ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_crossroads_to_gue_tech_outside(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

    def test_access_crossroads_to_hades_shore(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_crossroads_to_port_foozle(self) -> None:
        self._go_to_crossroads()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE.value))

    def test_access_crossroads_to_spell_lab_bridge(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_crossroads_to_subway_crossroads(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SUBWAY_TOKEN.value,
                ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS.value))

    def test_access_crossroads_to_subway_monastery(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_dm_lair_to_crossroads(self) -> None:
        self._go_to_dm_lair()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_dm_lair_to_dm_lair_interior(self) -> None:
        self._go_to_dm_lair()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY.value,
                ZorkGrandInquisitorItems.MEAD_LIGHT.value,
                ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value,
                ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR.value))

    def test_access_dm_lair_to_gue_tech_outside(self) -> None:
        self._go_to_dm_lair()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_dm_lair_to_hades_shore(self) -> None:
        self._go_to_dm_lair()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_dm_lair_to_spell_lab_bridge(self) -> None:
        self._go_to_dm_lair()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_dm_lair_to_subway_monastery(self) -> None:
        self._go_to_dm_lair()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_dm_lair_interior_to_dm_lair(self) -> None:
        self._go_to_dm_lair_interior()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_dm_lair_interior_to_walking_castle(self) -> None:
        self._go_to_dm_lair_interior()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.WALKING_CASTLE.value))

        self._obtain_obidil()

        self.collect_by_name(ZorkGrandInquisitorItems.HOTSPOT_BLINDS.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.WALKING_CASTLE.value))

    def test_access_dm_lair_interior_to_white_house(self) -> None:
        self._go_to_dm_lair_interior()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.WHITE_HOUSE.value))

        self._obtain_yastard()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR.value,
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.WHITE_HOUSE.value))

    def test_access_dragon_archipelago_to_dragon_archipelago_dragon(self) -> None:
        self._go_to_dragon_archipelago()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_GRIFF.value,
                ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON.value))

    def test_access_dragon_archipelago_to_hades_beyond_gates(self) -> None:
        self._go_to_dragon_archipelago()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_BEYOND_GATES.value))

    def test_access_dragon_archipelago_dragon_to_dragon_archipelago(self) -> None:
        self._go_to_dragon_archipelago_dragon()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO.value))

    def test_access_dragon_archipelago_dragon_to_endgame(self) -> None:
        self._go_to_dragon_archipelago_dragon()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value,
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value,
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value,
                ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value,
                ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value,
            )
        )

        self._go_to_port_foozle_past_tavern()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value,
                ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value,
                ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value,
            )
        )

        self._go_to_white_house()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_BROG.value,
                ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH.value,
                ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value,
                ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value,
                ZorkGrandInquisitorItems.BROGS_PLANK.value,
                ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

    def test_access_gue_tech_to_crossroads(self) -> None:
        self._go_to_gue_tech()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_gue_tech_to_gue_tech_hallway(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_IGRAM.value,
                ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY.value))

    def test_access_gue_tech_to_gue_tech_outside(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

        self.collect_by_name(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

    def test_access_gue_tech_hallway_to_gue_tech(self) -> None:
        self._go_to_gue_tech_hallway()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_gue_tech_hallway_to_spell_lab_bridge(self) -> None:
        self._go_to_gue_tech_hallway()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.STUDENT_ID.value,
                ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_gue_tech_outside_to_crossroads(self) -> None:
        self._go_to_gue_tech_outside()

        # Direct connection requires the map but indirect connection is free
        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_gue_tech_outside_to_dm_lair(self) -> None:
        self._go_to_gue_tech_outside()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_gue_tech_outside_to_gue_tech(self) -> None:
        self._go_to_gue_tech_outside()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_gue_tech_outside_to_hades_shore(self) -> None:
        self._go_to_gue_tech_outside()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_gue_tech_outside_to_spell_lab_bridge(self) -> None:
        self._go_to_gue_tech_outside()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_gue_tech_outside_to_subway_monastery(self) -> None:
        self._go_to_gue_tech_outside()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_hades_to_hades_beyond_gates(self) -> None:
        self._go_to_hades()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_BEYOND_GATES.value))

        self._obtain_snavig()

        self.collect_by_name(ZorkGrandInquisitorItems.TOTEM_BROG.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_BEYOND_GATES.value))

    def test_access_hades_to_hades_shore(self) -> None:
        self._go_to_hades()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_hades_beyond_gates_to_dragon_archipelago(self) -> None:
        self._go_to_hades_beyond_gates()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO.value))

        self._obtain_yastard()

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_NARWILE.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO.value))

    def test_access_hades_beyond_gates_to_hades(self) -> None:
        self._go_to_hades_beyond_gates()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES.value))

    def test_access_hades_shore_to_crossroads(self) -> None:
        self._go_to_hades_shore()

        # Direct connection requires the map but indirect connection is free
        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_hades_shore_to_dm_lair(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_hades_shore_to_gue_tech_outside(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

    def test_access_hades_shore_to_hades(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER.value,
                ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS.value,
                ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES.value))

    def test_access_hades_shore_to_spell_lab_bridge(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_hades_shore_to_subway_crossroads(self) -> None:
        self._go_to_hades_shore()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS.value))

    def test_access_hades_shore_to_subway_flood_control_dam(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value))

    def test_access_hades_shore_to_subway_monastery(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_monastery_to_hades_shore(self) -> None:
        self._go_to_monastery()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL.value,
                ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value,
                ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_monastery_to_monastery_exhibit(self) -> None:
        self._go_to_monastery()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION.value,
                ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value,
                ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT.value))

    def test_access_monastery_to_subway_monastery(self) -> None:
        self._go_to_monastery()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_monastery_exhibit_to_monastery(self) -> None:
        self._go_to_monastery_exhibit()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY.value))

    def test_access_monastery_exhibit_to_port_foozle_past(self) -> None:
        self._go_to_monastery_exhibit()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST.value))

        self._obtain_yastard()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER.value,
                ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT.value,
                ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value,
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST.value))

    def test_access_port_foozle_to_crossroads(self) -> None:
        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value,
                ZorkGrandInquisitorItems.LANTERN.value,
                ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value,
                ZorkGrandInquisitorItems.ROPE.value,
                ZorkGrandInquisitorItems.HOTSPOT_WELL.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_port_foozle_to_port_foozle_jacks_shop(self) -> None:
        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value,
                ZorkGrandInquisitorItems.LANTERN.value,
                ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP.value))

    def test_access_port_foozle_jacks_shop_to_port_foozle(self) -> None:
        self._go_to_port_foozle_jacks_shop()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE.value))

    def test_access_port_foozle_past_to_monastery_exhibit(self) -> None:
        self._go_to_port_foozle_past()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT.value))

    def test_access_port_foozle_past_to_port_foozle_past_tavern(self) -> None:
        self._go_to_port_foozle_past()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_LUCY.value,
                ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN.value))

    def test_access_port_foozle_past_tavern_to_endgame(self) -> None:
        self._go_to_port_foozle_past_tavern()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value,
                ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value,
                ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value,
            )
        )

        self._go_to_dragon_archipelago_dragon()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value,
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value,
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value,
                ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value,
                ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value,
            )
        )

        self._go_to_white_house()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_BROG.value,
                ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH.value,
                ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value,
                ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value,
                ZorkGrandInquisitorItems.BROGS_PLANK.value,
                ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

    def test_access_port_foozle_past_tavern_to_port_foozle_past(self) -> None:
        self._go_to_port_foozle_past_tavern()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST.value))

    def test_access_spell_lab_to_spell_lab_bridge(self) -> None:
        self._go_to_spell_lab()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_spell_lab_bridge_to_crossroads(self) -> None:
        self._go_to_spell_lab_bridge()

        # Direct connection requires the map but indirect connection is free
        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_spell_lab_bridge_to_dm_lair(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_spell_lab_bridge_to_gue_tech_outside(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE.value))

    def test_access_spell_lab_bridge_to_gue_tech_hallway(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY.value))

    def test_access_spell_lab_bridge_to_hades_shore(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_spell_lab_bridge_to_spell_lab(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB.value))

        self._go_to_subway_flood_control_dam()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_REZROV.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value,
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
                ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB.value))

    def test_access_spell_lab_bridge_to_subway_monastery(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_subway_crossroads_to_crossroads(self) -> None:
        self._go_to_subway_crossroads()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_subway_crossroads_to_hades_shore(self) -> None:
        self._go_to_subway_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_KENDALL.value,
                ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_subway_crossroads_to_subway_flood_control_dam(self) -> None:
        self._go_to_subway_crossroads()

        self.assertFalse(
            self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value)
        )

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_KENDALL.value,
                ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value,
            )
        )

        self.assertTrue(
            self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value)
        )

    def test_access_subway_crossroads_to_subway_monastery(self) -> None:
        self._go_to_subway_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_KENDALL.value,
                ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_subway_flood_control_dam_to_hades_shore(self) -> None:
        self._go_to_subway_flood_control_dam()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_subway_flood_control_dam_to_subway_crossroads(self) -> None:
        self._go_to_subway_flood_control_dam()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS.value))

    def test_access_subway_flood_control_dam_to_subway_monastery(self) -> None:
        self._go_to_subway_flood_control_dam()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_subway_monastery_to_hades_shore(self) -> None:
        self._go_to_subway_monastery()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_subway_monastery_to_monastery(self) -> None:
        self._go_to_subway_monastery()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.SPELL_GLORF.value,
                ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_VENT.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY.value))

    def test_access_subway_monastery_to_subway_crossroads(self) -> None:
        self._go_to_subway_monastery()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS.value))

    def test_access_subway_monastery_to_subway_flood_control_dam(self) -> None:
        self._go_to_subway_monastery()

        self.assertFalse(
            self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value)
        )

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value)

        self.assertTrue(
            self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value)
        )

    def test_access_walking_castle_to_dm_lair_interior(self) -> None:
        self._go_to_walking_castle()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR.value))

    def test_access_white_house_to_dm_lair_interior(self) -> None:
        self._go_to_white_house()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR.value))

    def test_access_white_house_to_endgame(self) -> None:
        self._go_to_white_house()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_BROG.value,
                ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH.value,
                ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value,
                ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value,
                ZorkGrandInquisitorItems.BROGS_PLANK.value,
                ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE.value,
            )
        )

        self._go_to_dragon_archipelago_dragon()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value,
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value,
                ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value,
                ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value,
                ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value,
            )
        )

        self._go_to_port_foozle_past_tavern()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value,
                ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value,
                ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value,
                ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

    def _go_to_crossroads(self) -> None:
        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LANTERN.value,
                ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value,
                ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value,
                ZorkGrandInquisitorItems.ROPE.value,
                ZorkGrandInquisitorItems.HOTSPOT_WELL.value,
            )
        )

    def _go_to_dm_lair(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE.value,
            )
        )

    def _go_to_dm_lair_interior(self) -> None:
        self._go_to_dm_lair()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY.value,
                ZorkGrandInquisitorItems.MEAD_LIGHT.value,
                ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value,
                ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH.value,
            )
        )

    def _go_to_dragon_archipelago(self) -> None:
        self._go_to_hades_beyond_gates()
        self._obtain_yastard()

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_NARWILE.value)

    def _go_to_dragon_archipelago_dragon(self) -> None:
        self._go_to_dragon_archipelago()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_GRIFF.value,
                ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW.value,
            )
        )

    def _go_to_gue_tech(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_REZROV.value,
                ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR.value,
            )
        )

    def _go_to_gue_tech_hallway(self) -> None:
        self._go_to_gue_tech()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_IGRAM.value,
                ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value,
            )
        )

    def _go_to_gue_tech_outside(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

    def _go_to_hades(self) -> None:
        self._go_to_hades_shore()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER.value,
                ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS.value,
                ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value,
            )
        )

    def _go_to_hades_beyond_gates(self) -> None:
        self._go_to_hades()
        self._obtain_snavig()

        self.collect_by_name(ZorkGrandInquisitorItems.TOTEM_BROG.value)

    def _go_to_hades_shore(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,
            )
        )

    def _go_to_monastery(self) -> None:
        self._go_to_subway_monastery()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.SPELL_GLORF.value,
                ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_VENT.value,
            )
        )

    def _go_to_monastery_exhibit(self) -> None:
        self._go_to_monastery()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION.value,
                ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value,
                ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value,
            )
        )

    def _go_to_port_foozle_jacks_shop(self) -> None:
        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value,
                ZorkGrandInquisitorItems.LANTERN.value,
                ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value,
            )
        )

    def _go_to_port_foozle_past(self) -> None:
        self._go_to_monastery_exhibit()

        self._obtain_yastard()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER.value,
                ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT.value,
                ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value,
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
            )
        )

    def _go_to_port_foozle_past_tavern(self) -> None:
        self._go_to_port_foozle_past()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.TOTEM_LUCY.value,
                ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR.value,
            )
        )

    def _go_to_spell_lab(self) -> None:
        self._go_to_subway_flood_control_dam()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_REZROV.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value,
            )
        )

        self._go_to_spell_lab_bridge()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
                ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM.value,
            )
        )

    def _go_to_spell_lab_bridge(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,
            )
        )

    def _go_to_subway_crossroads(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SUBWAY_TOKEN.value,
                ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT.value,
            )
        )

    def _go_to_subway_flood_control_dam(self) -> None:
        self._go_to_subway_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_KENDALL.value,
                ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value,
            )
        )

    def _go_to_subway_monastery(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,
            )
        )

    def _go_to_white_house(self) -> None:
        self._go_to_dm_lair_interior()

        self._obtain_yastard()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR.value,
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
            )
        )

    def _go_to_walking_castle(self) -> None:
        self._go_to_dm_lair_interior()

        self._obtain_obidil()
        self.collect_by_name(ZorkGrandInquisitorItems.HOTSPOT_BLINDS.value)

    def _obtain_obidil(self) -> None:
        self._go_to_crossroads()
        self._go_to_gue_tech()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value,
                ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT.value,
                ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS.value,
            )
        )

        self._go_to_subway_flood_control_dam()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_REZROV.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value,
            )
        )

        self._go_to_spell_lab_bridge()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
                ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM.value,
                ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value,
            )
        )

    def _obtain_snavig(self) -> None:
        self._go_to_crossroads()
        self._go_to_dm_lair_interior()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS.value,
                ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV.value,
                ZorkGrandInquisitorItems.HOTSPOT_MIRROR.value,
            )
        )

        self._go_to_subway_flood_control_dam()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_REZROV.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value,
                ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value,
            )
        )

        self._go_to_spell_lab_bridge()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
                ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM.value,
                ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value,
            )
        )

    def _obtain_yastard(self) -> None:
        self._go_to_crossroads()
        self._go_to_dm_lair_interior()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.FLATHEADIA_FUDGE.value,
                ZorkGrandInquisitorItems.HUNGUS_LARD.value,
                ZorkGrandInquisitorItems.JAR_OF_HOTBUGS.value,
                ZorkGrandInquisitorItems.QUELBEE_HONEYCOMB.value,
                ZorkGrandInquisitorItems.MOSS_OF_MAREILON.value,
                ZorkGrandInquisitorItems.MUG.value,
            )
        )


class AccessTestLocations(ZorkGrandInquisitorTestBase):
    options = {
        "deathsanity": "true",
        "start_with_hotspot_items": "false",
    }

    def test_access_locations_requiring_brogs_flickering_torch(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH.value,)]
        )

    def test_access_locations_requiring_brogs_grue_egg(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.BROGS_GRUE_EGG.value,)]
        )

    def test_access_locations_requiring_brogs_plank(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.BROGS_PLANK.value,)]
        )

    def test_access_locations_requiring_flatheadia_fudge(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.FLATHEADIA_FUDGE.value,)]
        )

    def test_access_locations_requiring_griffs_air_pump(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP.value,)]
        )

    def test_access_locations_requiring_griffs_dragon_tooth(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH.value,)]
        )

    def test_access_locations_requiring_griffs_inflatable_raft(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT.value,)]
        )

    def test_access_locations_requiring_griffs_inflatable_sea_captain(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN.value,)]
        )

    def test_access_locations_requiring_hammer(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BOING_BOING_BOING.value,
            ZorkGrandInquisitorLocations.BONK.value,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE.value,
            ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED.value,
            ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HAMMER.value,)]
        )

    def test_access_locations_requiring_hungus_lard(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HUNGUS_LARD.value,)]
        )

    def test_access_locations_requiring_jar_of_hotbugs(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.JAR_OF_HOTBUGS.value,)]
        )

    def test_access_locations_requiring_lantern(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.CIGAR_ACCESSIBLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LANTERN.value,)]
        )

    def test_access_locations_requiring_large_telegraph_hammer(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value,)]
        )

    def test_access_locations_requiring_lucys_playing_cards(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1.value,)]
        )

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2.value,)]
        )

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3.value,)]
        )

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4.value,)]
        )

    def test_access_locations_requiring_map(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.MAP.value,)]
        )

    def test_access_locations_requiring_mead_light(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.MEAD_LIGHT.value,
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.MEAD_LIGHT.value,)]
        )

    def test_access_locations_requiring_moss_of_mareilon(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.MOSS_OF_MAREILON.value,)]
        )

    def test_access_locations_requiring_mug(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.MUG.value,)]
        )

    def test_access_locations_requiring_old_scratch_card(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_SOUL_TO_OLD_SCRATCH.value,
            ZorkGrandInquisitorLocations.OLD_SCRATCH_WINNER.value,
            ZorkGrandInquisitorEvents.ZORKMID_BILL_ACCESSIBLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.OLD_SCRATCH_CARD.value,)]
        )

    def test_access_locations_requiring_perma_suck_machine(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.SUCKING_ROCKS.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE.value,)]
        )

    def test_access_locations_requiring_plastic_six_pack_holder(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE.value,
            ZorkGrandInquisitorLocations.WHAT_ARE_YOU_STUPID.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER.value,)]
        )

    def test_access_locations_requiring_pouch_of_zorkmids(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER.value,
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON.value,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.I_SPIT_ON_YOUR_FILTHY_COINAGE.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.SOUVENIR.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_OBIDIL.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_SUCKABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value,)]
        )

    def test_access_locations_requiring_prozork_tablet(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.PROZORKED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.PROZORK_TABLET.value,)]
        )

    def test_access_locations_requiring_quelbee_honeycomb(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.QUELBEE_HONEYCOMB.value,)]
        )

    def test_access_locations_requiring_rope(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.ALARM_SYSTEM_IS_DOWN.value,
            ZorkGrandInquisitorLocations.ARTIFACTS_EXPLAINED.value,
            ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER.value,
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE.value,
            ZorkGrandInquisitorLocations.A_SMALLWAY.value,
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
            ZorkGrandInquisitorLocations.BEBURTT_DEMYSTIFIED.value,
            ZorkGrandInquisitorLocations.BETTER_SPELL_MANUFACTURING_IN_UNDER_10_MINUTES.value,
            ZorkGrandInquisitorLocations.BOING_BOING_BOING.value,
            ZorkGrandInquisitorLocations.BONK.value,
            ZorkGrandInquisitorLocations.BRAVE_SOULS_WANTED.value,
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.CASTLE_WATCHING_A_FIELD_GUIDE.value,
            ZorkGrandInquisitorLocations.CAVES_NOTES.value,
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.CRISIS_AVERTED.value,
            ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_CLIMBED_OUT_OF_THE_WELL.value,
            ZorkGrandInquisitorLocations.DEATH_EATEN_BY_A_GRUE.value,
            ZorkGrandInquisitorLocations.DEATH_JUMPED_IN_BOTTOMLESS_PIT.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_SLICED_UP_BY_THE_INVISIBLE_GUARD.value,
            ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY.value,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON.value,
            ZorkGrandInquisitorLocations.DEATH_ZORK_ROCKS_EXPLODED.value,
            ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER.value,
            ZorkGrandInquisitorLocations.DESPERATELY_SEEKING_TUTOR.value,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY.value,
            ZorkGrandInquisitorLocations.DOOOOOOWN.value,
            ZorkGrandInquisitorLocations.DOWN.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.EGGPLANTS.value,
            ZorkGrandInquisitorLocations.EMERGENCY_MAGICATRONIC_MESSAGE.value,
            ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP.value,
            ZorkGrandInquisitorLocations.FAT_LOT_OF_GOOD_THATLL_DO_YA.value,
            ZorkGrandInquisitorLocations.FLOOD_CONTROL_DAM_3_THE_NOT_REMOTELY_BORING_TALE.value,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.FROBUARY_3_UNDERGROUNDHOG_DAY.value,
            ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE.value,
            ZorkGrandInquisitorLocations.GUE_TECH_DEANS_LIST.value,
            ZorkGrandInquisitorLocations.GUE_TECH_ENTRANCE_EXAM.value,
            ZorkGrandInquisitorLocations.GUE_TECH_HEALTH_MEMO.value,
            ZorkGrandInquisitorLocations.GUE_TECH_MAGEMEISTERS.value,
            ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY.value,
            ZorkGrandInquisitorLocations.HELLO_THIS_IS_SHONA_FROM_GURTH_PUBLISHING.value,
            ZorkGrandInquisitorLocations.HEY_FREE_DIRT.value,
            ZorkGrandInquisitorLocations.HI_MY_NAME_IS_DOUG.value,
            ZorkGrandInquisitorLocations.HMMM_INFORMATIVE_YET_DEEPLY_DISTURBING.value,
            ZorkGrandInquisitorLocations.HOLD_ON_FOR_AN_IMPORTANT_MESSAGE.value,
            ZorkGrandInquisitorLocations.HOW_TO_HYPNOTIZE_YOURSELF.value,
            ZorkGrandInquisitorLocations.HOW_TO_WIN_AT_DOUBLE_FANUCCI.value,
            ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY.value,
            ZorkGrandInquisitorLocations.I_SPIT_ON_YOUR_FILTHY_COINAGE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE.value,
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE.value,
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST.value,
            ZorkGrandInquisitorLocations.INVISIBLE_FLOWERS.value,
            ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE.value,
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.LIT_SUNFLOWERS.value,
            ZorkGrandInquisitorLocations.MAGIC_FOREVER.value,
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL.value,
            ZorkGrandInquisitorLocations.MAKE_LOVE_NOT_WAR.value,
            ZorkGrandInquisitorLocations.MIKES_PANTS.value,
            ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED.value,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorLocations.NATURAL_AND_SUPERNATURAL_CREATURES_OF_QUENDOR.value,
            ZorkGrandInquisitorLocations.NO_BONDAGE.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorLocations.NOTHIN_LIKE_A_GOOD_STOGIE.value,
            ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.PERMASEAL.value,
            ZorkGrandInquisitorLocations.PLEASE_DONT_THROCK_THE_GRASS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.PROZORKED.value,
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG.value,
            ZorkGrandInquisitorLocations.RESTOCKED_ON_GRUESDAY.value,
            ZorkGrandInquisitorLocations.RIGHT_HELLO_YES_UH_THIS_IS_SNEFFLE.value,
            ZorkGrandInquisitorLocations.RIGHT_UH_SORRY_ITS_ME_AGAIN_SNEFFLE.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.SOUVENIR.value,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.SUCKING_ROCKS.value,
            ZorkGrandInquisitorLocations.TAMING_YOUR_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THATS_A_ROPE.value,
            ZorkGrandInquisitorLocations.THATS_IT_JUST_KEEP_HITTING_THOSE_BUTTONS.value,
            ZorkGrandInquisitorLocations.THATS_STILL_A_ROPE.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED.value,
            ZorkGrandInquisitorLocations.TIME_TRAVEL_FOR_DUMMIES.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorLocations.UMBRELLA_FLOWERS.value,
            ZorkGrandInquisitorLocations.UP.value,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN.value,
            ZorkGrandInquisitorLocations.UUUUUP.value,
            ZorkGrandInquisitorLocations.VOYAGE_OF_CAPTAIN_ZAHAB.value,
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE.value,
            ZorkGrandInquisitorLocations.YAD_GOHDNUORGREDNU_3_YRAUBORF.value,
            ZorkGrandInquisitorLocations.YOU_DONT_GO_MESSING_WITH_A_MANS_ZIPPER.value,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS.value,
            ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY.value,
            ZorkGrandInquisitorEvents.CHARON_CALLED.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
            ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value,
            ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_OBIDIL.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
            ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
            ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_SUCKABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.ROPE.value,)]
        )

    def test_access_locations_requiring_scroll_fragment_ans(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS.value,)]
        )

    def test_access_locations_requiring_scroll_fragment_giv(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV.value,)]
        )

    def test_access_locations_requiring_shovel(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.HEY_FREE_DIRT.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SHOVEL.value,)]
        )

    def test_access_locations_requiring_snapdragon(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BOING_BOING_BOING.value,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SNAPDRAGON.value,)]
        )

    def test_access_locations_requiring_student_id(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.STUDENT_ID.value,)]
        )

    def test_access_locations_requiring_subway_token(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SUBWAY_TOKEN.value,)]
        )

    def test_access_locations_requiring_sword(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY.value,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY.value,
            ZorkGrandInquisitorLocations.HMMM_INFORMATIVE_YET_DEEPLY_DISTURBING.value,
            ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE.value,
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE.value,
            ZorkGrandInquisitorLocations.MAKE_LOVE_NOT_WAR.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.PERMASEAL.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS.value,
            ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SWORD.value,)]
        )

    def test_access_locations_requiring_zimdor_scroll(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value,)]
        )

    def test_access_locations_requiring_zork_rocks(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.ZORK_ROCKS.value,)]
        )

    def test_access_locations_requiring_hotspot_666_mailbox(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX.value,)]
        )

    def test_access_locations_requiring_hotspot_alpines_quandry_card_slots(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS.value,)]
        )

    def test_access_locations_requiring_hotspot_blank_scroll_box(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX.value,)]
        )

    def test_access_locations_requiring_hotspot_blinds(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER.value,
            ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_BLINDS.value,)]
        )

    def test_access_locations_requiring_hotspot_candy_machine_buttons(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_SUCKABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS.value,)]
        )

    def test_access_locations_requiring_hotspot_candy_machine_coin_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_SUCKABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_candy_machine_vacuum_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.SUCKING_ROCKS.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_change_machine_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_closet_door(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.DOOOOOOWN.value,
            ZorkGrandInquisitorLocations.DOWN.value,
            ZorkGrandInquisitorLocations.UP.value,
            ZorkGrandInquisitorLocations.UUUUUP.value,
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL.value,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
            ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR.value,)]
        )

    def test_access_locations_requiring_hotspot_closing_the_time_tunnels_hammer_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_closing_the_time_tunnels_lever(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER.value,)]
        )

    def test_access_locations_requiring_hotspot_cooking_pot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT.value,)]
        )

    def test_access_locations_requiring_hotspot_dented_locker(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.CRISIS_AVERTED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER.value,)]
        )

    def test_access_locations_requiring_hotspot_dirt_mound(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.HEY_FREE_DIRT.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND.value,)]
        )

    def test_access_locations_requiring_hotspot_dock_winch(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE.value,
            ZorkGrandInquisitorLocations.NO_BONDAGE.value,
            ZorkGrandInquisitorLocations.YOU_WANT_A_PIECE_OF_ME_DOCK_BOY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH.value,)]
        )

    def test_access_locations_requiring_hotspot_dragon_claw(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW.value,)]
        )

    def test_access_locations_requiring_hotspot_dragon_nostrils(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS.value,)]
        )

    def test_access_locations_requiring_hotspot_dungeon_masters_lair_entrance(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE.value,)]
        )

    def test_access_locations_requiring_hotspot_flood_control_buttons(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS.value,)]
        )

    def test_access_locations_requiring_hotspot_flood_control_doors(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS.value,)]
        )

    def test_access_locations_requiring_hotspot_frozen_treat_machine_coin_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_OBIDIL.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_frozen_treat_machine_doors(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_OBIDIL.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS.value,)]
        )

    def test_access_locations_requiring_hotspot_glass_case(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE.value,)]
        )

    def test_access_locations_requiring_hotspot_grand_inquisitor_doll(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.ARREST_THE_VANDAL.value,
            ZorkGrandInquisitorLocations.DEATH_ARRESTED_WITH_JACK.value,
            ZorkGrandInquisitorLocations.FIRE_FIRE.value,
            ZorkGrandInquisitorLocations.PLANETFALL.value,
            ZorkGrandInquisitorLocations.TALK_TO_ME_GRAND_INQUISITOR.value,
            ZorkGrandInquisitorEvents.LANTERN_DALBOZ_ACCESSIBLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value,)]
        )

    def test_access_locations_requiring_hotspot_gue_tech_door(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR.value,)]
        )

    def test_access_locations_requiring_hotspot_gue_tech_grass(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS.value,)]
        )

    def test_access_locations_requiring_hotspot_hades_phone_buttons(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER.value,
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE.value,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY.value,
            ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorEvents.CHARON_CALLED.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS.value,)]
        )

    def test_access_locations_requiring_hotspot_hades_phone_receiver(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER.value,
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE.value,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY.value,
            ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorEvents.CHARON_CALLED.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER.value,)]
        )

    def test_access_locations_requiring_hotspot_harry(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_HARRY.value,)]
        )

    def test_access_locations_requiring_hotspot_harrys_ashtray(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.NOTHIN_LIKE_A_GOOD_STOGIE.value,
            ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY.value,)]
        )

    def test_access_locations_requiring_hotspot_harrys_bird_bath(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH.value,)]
        )

    def test_access_locations_requiring_hotspot_in_magic_we_trust_door(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR.value,)]
        )

    def test_access_locations_requiring_hotspot_jacks_door(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.MEAD_LIGHT.value,
            ZorkGrandInquisitorLocations.NO_AUTOGRAPHS.value,
            ZorkGrandInquisitorLocations.THATS_A_ROPE.value,
            ZorkGrandInquisitorLocations.WHAT_ARE_YOU_STUPID.value,
            ZorkGrandInquisitorEvents.CIGAR_ACCESSIBLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value,)]
        )

    def test_access_locations_requiring_hotspot_loudspeaker_volume_buttons(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.THATS_THE_SPIRIT.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS.value,)]
        )

    def test_access_locations_requiring_hotspot_mailbox_door(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL.value,
            ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR.value,)]
        )

    def test_access_locations_requiring_hotspot_mailbox_flag(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DOOOOOOWN.value,
            ZorkGrandInquisitorLocations.DOWN.value,
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL.value,
            ZorkGrandInquisitorLocations.UP.value,
            ZorkGrandInquisitorLocations.UUUUUP.value,
            ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG.value,)]
        )

    def test_access_locations_requiring_hotspot_mirror(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG.value,
            ZorkGrandInquisitorLocations.YAD_GOHDNUORGREDNU_3_YRAUBORF.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_MIRROR.value,)]
        )

    def test_access_locations_requiring_hotspot_monastery_vent(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY.value,
            ZorkGrandInquisitorLocations.HMMM_INFORMATIVE_YET_DEEPLY_DISTURBING.value,
            ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PERMASEAL.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_VENT.value,)]
        )

    def test_access_locations_requiring_hotspot_mossy_grate(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE.value,)]
        )

    def test_access_locations_requiring_hotspot_port_foozle_past_tavern_door(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR.value,)]
        )

    def test_access_locations_requiring_hotspot_purple_words(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_SMALLWAY.value,
            ZorkGrandInquisitorLocations.CRISIS_AVERTED.value,
            ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS.value,)]
        )

    def test_access_locations_requiring_hotspot_quelbee_hive(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE.value,)]
        )

    def test_access_locations_requiring_hotspot_rope_bridge(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE.value,)]
        )

    def test_access_locations_requiring_hotspot_skull_cage(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE.value,)]
        )

    def test_access_locations_requiring_hotspot_snapdragon(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BONK.value,
            ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY.value,
            ZorkGrandInquisitorLocations.PROZORKED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON.value,)]
        )

    def test_access_locations_requiring_hotspot_soda_machine_buttons(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS.value,)]
        )

    def test_access_locations_requiring_hotspot_soda_machine_coin_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_souvenir_coin_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.SOUVENIR.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_spell_checker(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER.value,)]
        )

    def test_access_locations_requiring_hotspot_spell_lab_chasm(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM.value,)]
        )

    def test_access_locations_requiring_hotspot_spring_mushroom(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BOING_BOING_BOING.value,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED.value,
            ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM.value,)]
        )

    def test_access_locations_requiring_hotspot_student_id_machine(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE.value,)]
        )

    def test_access_locations_requiring_hotspot_subway_token_slot(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT.value,)]
        )

    def test_access_locations_requiring_hotspot_tavern_fly(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY.value,)]
        )

    def test_access_locations_requiring_hotspot_totemizer_switch(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH.value,)]
        )

    def test_access_locations_requiring_hotspot_totemizer_wheels(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS.value,)]
        )

    def test_access_locations_requiring_hotspot_well(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.ALARM_SYSTEM_IS_DOWN.value,
            ZorkGrandInquisitorLocations.ARTIFACTS_EXPLAINED.value,
            ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER.value,
            ZorkGrandInquisitorLocations.A_LETTER_FROM_THE_WHITE_HOUSE.value,
            ZorkGrandInquisitorLocations.A_SMALLWAY.value,
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
            ZorkGrandInquisitorLocations.BEBURTT_DEMYSTIFIED.value,
            ZorkGrandInquisitorLocations.BETTER_SPELL_MANUFACTURING_IN_UNDER_10_MINUTES.value,
            ZorkGrandInquisitorLocations.BOING_BOING_BOING.value,
            ZorkGrandInquisitorLocations.BONK.value,
            ZorkGrandInquisitorLocations.BRAVE_SOULS_WANTED.value,
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.CASTLE_WATCHING_A_FIELD_GUIDE.value,
            ZorkGrandInquisitorLocations.CAVES_NOTES.value,
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.CRISIS_AVERTED.value,
            ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_CLIMBED_OUT_OF_THE_WELL.value,
            ZorkGrandInquisitorLocations.DEATH_EATEN_BY_A_GRUE.value,
            ZorkGrandInquisitorLocations.DEATH_JUMPED_IN_BOTTOMLESS_PIT.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_SLICED_UP_BY_THE_INVISIBLE_GUARD.value,
            ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY.value,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON.value,
            ZorkGrandInquisitorLocations.DEATH_ZORK_ROCKS_EXPLODED.value,
            ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER.value,
            ZorkGrandInquisitorLocations.DESPERATELY_SEEKING_TUTOR.value,
            ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY.value,
            ZorkGrandInquisitorLocations.DOOOOOOWN.value,
            ZorkGrandInquisitorLocations.DOWN.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.EGGPLANTS.value,
            ZorkGrandInquisitorLocations.EMERGENCY_MAGICATRONIC_MESSAGE.value,
            ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP.value,
            ZorkGrandInquisitorLocations.FAT_LOT_OF_GOOD_THATLL_DO_YA.value,
            ZorkGrandInquisitorLocations.FLOOD_CONTROL_DAM_3_THE_NOT_REMOTELY_BORING_TALE.value,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.FROBUARY_3_UNDERGROUNDHOG_DAY.value,
            ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE.value,
            ZorkGrandInquisitorLocations.GUE_TECH_DEANS_LIST.value,
            ZorkGrandInquisitorLocations.GUE_TECH_ENTRANCE_EXAM.value,
            ZorkGrandInquisitorLocations.GUE_TECH_HEALTH_MEMO.value,
            ZorkGrandInquisitorLocations.GUE_TECH_MAGEMEISTERS.value,
            ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY.value,
            ZorkGrandInquisitorLocations.HELLO_THIS_IS_SHONA_FROM_GURTH_PUBLISHING.value,
            ZorkGrandInquisitorLocations.HEY_FREE_DIRT.value,
            ZorkGrandInquisitorLocations.HI_MY_NAME_IS_DOUG.value,
            ZorkGrandInquisitorLocations.HMMM_INFORMATIVE_YET_DEEPLY_DISTURBING.value,
            ZorkGrandInquisitorLocations.HOLD_ON_FOR_AN_IMPORTANT_MESSAGE.value,
            ZorkGrandInquisitorLocations.HOW_TO_HYPNOTIZE_YOURSELF.value,
            ZorkGrandInquisitorLocations.HOW_TO_WIN_AT_DOUBLE_FANUCCI.value,
            ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY.value,
            ZorkGrandInquisitorLocations.I_SPIT_ON_YOUR_FILTHY_COINAGE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE.value,
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE.value,
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST.value,
            ZorkGrandInquisitorLocations.INVISIBLE_FLOWERS.value,
            ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE.value,
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.LIT_SUNFLOWERS.value,
            ZorkGrandInquisitorLocations.MAGIC_FOREVER.value,
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL.value,
            ZorkGrandInquisitorLocations.MAKE_LOVE_NOT_WAR.value,
            ZorkGrandInquisitorLocations.MIKES_PANTS.value,
            ZorkGrandInquisitorLocations.MUSHROOM_HAMMERED.value,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorLocations.NATURAL_AND_SUPERNATURAL_CREATURES_OF_QUENDOR.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorLocations.NOTHIN_LIKE_A_GOOD_STOGIE.value,
            ZorkGrandInquisitorLocations.NOW_YOU_LOOK_LIKE_US_WHICH_IS_AN_IMPROVEMENT.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.OH_WOW_TALK_ABOUT_DEJA_VU.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.PERMASEAL.value,
            ZorkGrandInquisitorLocations.PLEASE_DONT_THROCK_THE_GRASS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.PROZORKED.value,
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG.value,
            ZorkGrandInquisitorLocations.RESTOCKED_ON_GRUESDAY.value,
            ZorkGrandInquisitorLocations.RIGHT_HELLO_YES_UH_THIS_IS_SNEFFLE.value,
            ZorkGrandInquisitorLocations.RIGHT_UH_SORRY_ITS_ME_AGAIN_SNEFFLE.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.SOUVENIR.value,
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.SUCKING_ROCKS.value,
            ZorkGrandInquisitorLocations.TAMING_YOUR_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THATS_IT_JUST_KEEP_HITTING_THOSE_BUTTONS.value,
            ZorkGrandInquisitorLocations.THATS_STILL_A_ROPE.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED.value,
            ZorkGrandInquisitorLocations.TIME_TRAVEL_FOR_DUMMIES.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorLocations.UMBRELLA_FLOWERS.value,
            ZorkGrandInquisitorLocations.UP.value,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN.value,
            ZorkGrandInquisitorLocations.UUUUUP.value,
            ZorkGrandInquisitorLocations.VOYAGE_OF_CAPTAIN_ZAHAB.value,
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE.value,
            ZorkGrandInquisitorLocations.YAD_GOHDNUORGREDNU_3_YRAUBORF.value,
            ZorkGrandInquisitorLocations.YOU_DONT_GO_MESSING_WITH_A_MANS_ZIPPER.value,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS.value,
            ZorkGrandInquisitorLocations.YOUR_PUNY_WEAPONS_DONT_PHASE_ME_BABY.value,
            ZorkGrandInquisitorEvents.CHARON_CALLED.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
            ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value,
            ZorkGrandInquisitorEvents.DALBOZ_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_OBIDIL.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD.value,
            ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
            ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_SUCKABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HOTSPOT_WELL.value,)]
        )

    def test_access_locations_requiring_spell_glorf(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_GLORF.value,)]
        )

    def test_access_locations_requiring_spell_golgatem(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DENIED_BY_THE_LAKE_MONSTER.value,
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.OBIDIL_DRIED_UP.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,)]
        )

    def test_access_locations_requiring_spell_igram(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_SMALLWAY.value,
            ZorkGrandInquisitorLocations.CRISIS_AVERTED.value,
            ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE.value,
            ZorkGrandInquisitorLocations.FAT_LOT_OF_GOOD_THATLL_DO_YA.value,
            ZorkGrandInquisitorLocations.INVISIBLE_FLOWERS.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_IGRAM.value,)]
        )

    def test_access_locations_requiring_spell_kendall(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BEBURTT_DEMYSTIFIED.value,
            ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_KENDALL.value,)]
        )

    def test_access_locations_requiring_spell_narwile(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DOOOOOOWN.value,
            ZorkGrandInquisitorLocations.DOWN.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorLocations.UP.value,
            ZorkGrandInquisitorLocations.UUUUUP.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
            ZorkGrandInquisitorEvents.WHITE_HOUSE_LETTER_MAILABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_NARWILE.value,)]
        )

    def test_access_locations_requiring_spell_rezrov(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST.value,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorLocations.YOU_DONT_GO_MESSING_WITH_A_MANS_ZIPPER.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_REZROV.value,)]
        )

    def test_access_locations_requiring_spell_throck(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
            ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS.value,
            ZorkGrandInquisitorLocations.FLYING_SNAPDRAGON.value,
            ZorkGrandInquisitorLocations.I_DONT_THINK_YOU_WOULDVE_WANTED_THAT_TO_WORK_ANYWAY.value,
            ZorkGrandInquisitorLocations.LIT_SUNFLOWERS.value,
            ZorkGrandInquisitorLocations.THROCKED_MUSHROOM_HAMMERED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_THROCK.value,)]
        )

    def test_access_locations_requiring_subway_destination_flood_control_dam(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
            ZorkGrandInquisitorLocations.FLOOD_CONTROL_DAM_3_THE_NOT_REMOTELY_BORING_TALE.value,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorLocations.SOUVENIR.value,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value,)]
        )

    def test_access_locations_requiring_subway_destination_hades(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES.value,)]
        )

    def test_access_locations_requiring_subway_destination_monastery(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value,)]
        )

    def test_access_locations_requiring_teleporter_destination_dm_lair(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value,)]
        )

    def test_access_locations_requiring_teleporter_destination_gue_tech(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,)]
        )

    def test_access_locations_requiring_teleporter_destination_hades(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,)]
        )

    def test_access_locations_requiring_teleporter_destination_monastery(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,)]
        )

    def test_access_locations_requiring_teleporter_destination_spell_lab(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,)]
        )

    def test_access_locations_requiring_totemizer_destination_hall_of_inquisition(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.CLOSING_THE_TIME_TUNNELS.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THE_ALCHEMICAL_DEBACLE.value,
            ZorkGrandInquisitorLocations.THE_ENDLESS_FIRE.value,
            ZorkGrandInquisitorLocations.THE_FLATHEADIAN_FUDGE_FIASCO.value,
            ZorkGrandInquisitorLocations.THE_PERILS_OF_MAGIC.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION.value,)]
        )

    def test_access_locations_requiring_totemizer_destination_straight_to_hell(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.STRAIGHT_TO_HELL.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL.value,)]
        )

    def test_access_locations_requiring_totem_brog(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_EAT_ROCKS.value,
            ZorkGrandInquisitorLocations.BROG_KNOW_DUMB_THAT_DUMB.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_VERY_FUNNY_GUYS.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.UH_OH_BROG_CANT_SWIM.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEM_BROG.value,)]
        )

    def test_access_locations_requiring_totem_griff(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DOOOOOOWN.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.UUUUUP.value,
            ZorkGrandInquisitorLocations.WE_DONT_SERVE_YOUR_KIND_HERE.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEM_GRIFF.value,)]
        )

    def test_access_locations_requiring_totem_lucy(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DOWN.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THIS_DOESNT_LOOK_ANYTHING_LIKE_THE_BROCHURE.value,
            ZorkGrandInquisitorLocations.UP.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEM_LUCY.value,)]
        )
