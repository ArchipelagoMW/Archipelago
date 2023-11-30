from typing import List

from . import ZorkGrandInquisitorTestBase

from ..enums import (
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
)


class AccessTestRegions(ZorkGrandInquisitorTestBase):
    def test_access_crossroads_to_dm_lair_sword(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SWORD.value)

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

    def test_access_crossroads_to_gue_tech_rezrov(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_REZROV.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_crossroads_to_gue_tech_teleporter(self) -> None:
        self._go_to_crossroads()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

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

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_TOKEN.value)

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
                ZorkGrandInquisitorItems.MEAD_LIGHT.value,
                ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR.value))

    def test_access_dm_lair_to_gue_tech(self) -> None:
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

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_OBIDIL.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.WALKING_CASTLE.value))

    def test_access_dm_lair_interior_to_white_house(self) -> None:
        self._go_to_dm_lair_interior()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.WHITE_HOUSE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
                ZorkGrandInquisitorItems.TOTEM_BROG.value,
                ZorkGrandInquisitorItems.SPELL_YASTARD.value,
                ZorkGrandInquisitorItems.REVEALED_BROGS_TIME_TUNNEL_ITEMS.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.WHITE_HOUSE.value))

    def test_access_dragon_archipelago_to_endgame(self) -> None:
        self._go_to_dragon_archipelago()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

        self._go_to_port_foozle_past()
        self._go_to_white_house()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

    def test_access_dragon_archipelago_to_hades_beyond_gates(self) -> None:
        self._go_to_dragon_archipelago()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_BEYOND_GATES.value))

    def test_access_gue_tech_to_crossroads(self) -> None:
        self._go_to_gue_tech()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_gue_tech_to_dm_lair(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DM_LAIR.value))

    def test_access_gue_tech_to_gue_tech_hallway(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_IGRAM.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY.value))

    def test_access_gue_tech_to_hades_shore(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_gue_tech_to_spell_lab_bridge(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_gue_tech_to_subway_monastery(self) -> None:
        self._go_to_gue_tech()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_gue_tech_hallway_to_gue_tech(self) -> None:
        self._go_to_gue_tech_hallway()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_gue_tech_hallway_to_spell_lab_bridge(self) -> None:
        self._go_to_gue_tech_hallway()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

        self.collect_by_name(ZorkGrandInquisitorItems.STUDENT_ID.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_hades_to_hades_beyond_gates(self) -> None:
        self._go_to_hades()

        self.assertFalse(
            self.can_reach_region(ZorkGrandInquisitorRegions.HADES_BEYOND_GATES.value)
        )

        self._obtain_snavig()
        self.collect_by_name(ZorkGrandInquisitorItems.TOTEM_BROG.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_BEYOND_GATES.value))

    def test_access_hades_to_hades_shore(self) -> None:
        self._go_to_hades()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_hades_beyond_gates_to_dragon_archipelago(self) -> None:
        self._go_to_hades_beyond_gates()

        self.assertFalse(
            self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO.value)
        )

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
                ZorkGrandInquisitorItems.TOTEM_GRIFF.value,
                ZorkGrandInquisitorItems.SPELL_YASTARD.value,
                ZorkGrandInquisitorItems.REVEALED_GRIFFS_TIME_TUNNEL_ITEMS.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO.value))

    def test_access_hades_beyond_gates_to_hades(self) -> None:
        self._go_to_hades_beyond_gates()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES.value))

    def test_access_hades_shore_to_crossroads(self) -> None:
        self._go_to_hades_shore()

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

    def test_access_hades_shore_to_gue_tech(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

    def test_access_hades_shore_to_hades(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.HADES.value))

        self.collect_by_name(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value)

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

        self.assertFalse(
            self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value)
        )

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM.value)

        self.assertTrue(
            self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM.value)
        )

    def test_access_hades_shore_to_subway_monastery(self) -> None:
        self._go_to_hades_shore()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY.value)

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_monastery_to_hades_shore(self) -> None:
        self._go_to_monastery()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.HADES_SHORE.value))

    def test_access_monastery_to_port_foozle_past(self) -> None:
        self._go_to_monastery()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value,
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
                ZorkGrandInquisitorItems.TOTEM_LUCY.value,
                ZorkGrandInquisitorItems.SPELL_YASTARD.value,
                ZorkGrandInquisitorItems.REVEALED_LUCYS_TIME_TUNNEL_ITEMS.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST.value))

    def test_access_monastery_to_subway_monastery(self) -> None:
        self._go_to_monastery()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SUBWAY_MONASTERY.value))

    def test_access_port_foozle_to_crossroads(self) -> None:
        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.ROPE.value,
                ZorkGrandInquisitorItems.LANTERN.value,
            )
        )

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.CROSSROADS.value))

    def test_access_port_foozle_to_port_foozle_jacks_shop(self) -> None:
        self.assertFalse(
            self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP.value)
        )

        self.collect_by_name(ZorkGrandInquisitorItems.LANTERN.value)

        self.assertTrue(
            self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP.value)
        )

    def test_access_port_foozle_jacks_shop_to_port_foozle(self) -> None:
        self._go_to_port_foozle_jacks_shop()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.PORT_FOOZLE.value))

    def test_access_port_foozle_past_to_endgame(self) -> None:
        self._go_to_port_foozle_past()

        self.assertFalse(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

        self._go_to_dragon_archipelago()
        self._go_to_white_house()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

    def test_access_port_foozle_past_to_monastery(self) -> None:
        self._go_to_port_foozle_past()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.MONASTERY.value))

    def test_access_spell_lab_to_spell_lab_bridge(self) -> None:
        self._go_to_spell_lab()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE.value))

    def test_access_spell_lab_bridge_to_crossroads(self) -> None:
        self._go_to_spell_lab_bridge()

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

    def test_access_spell_lab_bridge_to_gue_tech(self) -> None:
        self._go_to_spell_lab_bridge()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.GUE_TECH.value))

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
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
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

        self._go_to_dragon_archipelago()
        self._go_to_port_foozle_past()

        self.assertTrue(self.can_reach_region(ZorkGrandInquisitorRegions.ENDGAME.value))

    def _go_to_crossroads(self) -> None:
        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LANTERN.value,
                ZorkGrandInquisitorItems.ROPE.value,
            )
        )

    def _go_to_dm_lair(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(ZorkGrandInquisitorItems.SWORD.value)

    def _go_to_dm_lair_interior(self) -> None:
        self._go_to_dm_lair()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MEAD_LIGHT.value,
                ZorkGrandInquisitorItems.ZIMDOR_SCROLL.value,
            )
        )

    def _go_to_dragon_archipelago(self) -> None:
        self._go_to_hades_beyond_gates()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
                ZorkGrandInquisitorItems.TOTEM_GRIFF.value,
                ZorkGrandInquisitorItems.SPELL_YASTARD.value,
                ZorkGrandInquisitorItems.REVEALED_GRIFFS_TIME_TUNNEL_ITEMS.value,
            )
        )

    def _go_to_gue_tech(self) -> None:
        self._go_to_crossroads()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.MAP.value,
                ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH.value,
            )
        )

    def _go_to_gue_tech_hallway(self) -> None:
        self._go_to_gue_tech()

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_IGRAM.value)

    def _go_to_hades(self) -> None:
        self._go_to_hades_shore()

        self.collect_by_name(ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS.value)

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
            )
        )

    def _go_to_port_foozle_jacks_shop(self) -> None:
        self.collect_by_name(ZorkGrandInquisitorItems.LANTERN.value)

    def _go_to_port_foozle_past(self) -> None:
        self._go_to_monastery()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value,
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
                ZorkGrandInquisitorItems.TOTEM_LUCY.value,
                ZorkGrandInquisitorItems.SPELL_YASTARD.value,
                ZorkGrandInquisitorItems.REVEALED_LUCYS_TIME_TUNNEL_ITEMS.value,
            )
        )

    def _go_to_spell_lab(self) -> None:
        self._go_to_subway_flood_control_dam()

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_REZROV.value)

        self._go_to_spell_lab_bridge()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
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

        self.collect_by_name(ZorkGrandInquisitorItems.SUBWAY_TOKEN.value)

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

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_NARWILE.value,
                ZorkGrandInquisitorItems.TOTEM_BROG.value,
                ZorkGrandInquisitorItems.SPELL_YASTARD.value,
                ZorkGrandInquisitorItems.REVEALED_BROGS_TIME_TUNNEL_ITEMS.value,
            )
        )

    def _go_to_walking_castle(self) -> None:
        self._go_to_dm_lair_interior()

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_OBIDIL.value)

    def _obtain_snavig(self) -> None:
        self._go_to_crossroads()
        self._go_to_dm_lair()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SPELL_THROCK.value,
                ZorkGrandInquisitorItems.SNAPDRAGON.value,
                ZorkGrandInquisitorItems.HAMMER.value,
            )
        )

        self._go_to_dm_lair_interior()
        self._go_to_subway_flood_control_dam()

        self.collect_by_name(ZorkGrandInquisitorItems.SPELL_REZROV.value)

        self._go_to_spell_lab_bridge()

        self.collect_by_name(
            (
                ZorkGrandInquisitorItems.SWORD.value,
                ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,
            )
        )


class AccessTestLocations(ZorkGrandInquisitorTestBase):
    options = {
        "deathsanity": "true",
    }

    def test_access_locations_requiring_hammer(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorEvents.HAS_HALF_OF_SNAVIG.value,
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE.value,
            ZorkGrandInquisitorLocations.PLANTS_ARE_MANS_BEST_FRIEND.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HAMMER.value,)]
        )

    def test_access_locations_requiring_hungus_lard(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.HUNGUS_LARD.value,)]
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
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER.value,)]
        )

    def test_access_locations_requiring_map(self) -> None:
        locations: List[str] = list()

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.MAP.value,)]
        )

    def test_access_locations_requiring_mead_light(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.MEAD_LIGHT.value,)]
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
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER.value,)]
        )

    def test_access_locations_requiring_pouch_of_zorkmids(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.SOUVENIR.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
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

    def test_access_locations_requiring_rope(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.ARTIFACTS_EXPLAINED.value,
            ZorkGrandInquisitorLocations.A_SMALLWAY.value,
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
            ZorkGrandInquisitorLocations.BEBURTT_DEMYSTIFIED.value,
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
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
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.DUNCE_LOCKER.value,
            ZorkGrandInquisitorLocations.ENJOY_YOUR_TRIP.value,
            ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE.value,
            ZorkGrandInquisitorLocations.GUE_TECH_ENTRANCE_EXAM.value,
            ZorkGrandInquisitorLocations.HAVE_A_HELL_OF_A_DAY.value,
            ZorkGrandInquisitorLocations.HEY_FREE_DIRT.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE.value,
            ZorkGrandInquisitorLocations.IN_CASE_OF_ADVENTURE.value,
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST.value,
            ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE.value,
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.MAGIC_FOREVER.value,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorLocations.NOOOOOOOOOOOOO.value,
            ZorkGrandInquisitorLocations.NOTHIN_LIKE_A_GOOD_STOGIE.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OPEN_THE_GATES_OF_HELL.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.PLANTS_ARE_MANS_BEST_FRIEND.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.PROZORKED.value,
            ZorkGrandInquisitorLocations.REASSEMBLE_SNAVIG.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.SOUVENIR.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.SUCKING_ROCKS.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.THE_UNDERGROUND_UNDERGROUND.value,
            ZorkGrandInquisitorLocations.UMBRELLA_FLOWERS.value,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN.value,
            ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE.value,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD.value,
            ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR.value,
            ZorkGrandInquisitorEvents.DUNCE_LOCKER_OPENABLE.value,
            ZorkGrandInquisitorEvents.HAS_HALF_OF_SNAVIG.value,
            ZorkGrandInquisitorEvents.HAS_REPAIRABLE_SNAVIG.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
            ZorkGrandInquisitorEvents.ROPE_GLORFABLE.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_ACTIVATED.value,
            ZorkGrandInquisitorEvents.ZORK_ROCKS_SUCKABLE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.ROPE.value,)]
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
            ZorkGrandInquisitorLocations.PLANTS_ARE_MANS_BEST_FRIEND.value,
            ZorkGrandInquisitorEvents.HAS_HALF_OF_SNAVIG.value,
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
            ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED.value,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY.value,
            ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.INTO_THE_FOLIAGE.value,
            ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.YOU_GAINED_86_EXPERIENCE_POINTS.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
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

    def test_access_locations_requiring_revealed_brogs_time_tunnel_items(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.REVEALED_BROGS_TIME_TUNNEL_ITEMS.value,)]
        )

    def test_access_locations_requiring_revealed_griffs_time_tunnel_items(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.REVEALED_GRIFFS_TIME_TUNNEL_ITEMS.value,)]
        )

    def test_access_locations_requiring_revealed_lucys_time_tunnel_items(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.REVEALED_LUCYS_TIME_TUNNEL_ITEMS.value,)]
        )

    def test_access_locations_requiring_unlocked_blank_scroll_box_access(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.UNLOCKED_BLANK_SCROLL_BOX_ACCESS.value,)]
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
            ZorkGrandInquisitorLocations.I_LIKE_YOUR_STYLE.value,
            ZorkGrandInquisitorLocations.IMBUE_BEBURTT.value,
            ZorkGrandInquisitorLocations.SNAVIG_REPAIRED.value,
            ZorkGrandInquisitorLocations.USELESS_BUT_FUN.value,
            ZorkGrandInquisitorEvents.KNOWS_BEBURTT.value,
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_GOLGATEM.value,)]
        )

    def test_access_locations_requiring_spell_igram(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.A_SMALLWAY.value,
            ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE.value,
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
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.PORT_FOOZLE_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorLocations.WHITE_HOUSE_TIME_TUNNEL.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_NARWILE.value,)]
        )

    def test_access_locations_requiring_spell_obidil(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.WOW_IVE_NEVER_GONE_INSIDE_HIM_BEFORE.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_OBIDIL.value,)]
        )

    def test_access_locations_requiring_spell_rezrov(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST.value,
            ZorkGrandInquisitorLocations.NATIONAL_TREASURE.value,
            ZorkGrandInquisitorEvents.DAM_DESTROYED.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_REZROV.value,)]
        )

    def test_access_locations_requiring_spell_throck(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
            ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS.value,
            ZorkGrandInquisitorLocations.PLANTS_ARE_MANS_BEST_FRIEND.value,
            ZorkGrandInquisitorEvents.HAS_HALF_OF_SNAVIG.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_THROCK.value,)]
        )

    def test_access_locations_requiring_spell_yastard(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.SPELL_YASTARD.value,)]
        )

    def test_access_locations_requiring_subway_destination_flood_control_dam(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY.value,
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

    def test_access_locations_requiring_totem_brog(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.BROG_DO_GOOD.value,
            ZorkGrandInquisitorLocations.BROG_MUCH_BETTER_AT_THIS_GAME.value,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEM_BROG.value,)]
        )

    def test_access_locations_requiring_totem_griff(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON.value,
            ZorkGrandInquisitorLocations.OH_DEAR_GOD_ITS_A_DRAGON.value,
            ZorkGrandInquisitorLocations.THAR_SHE_BLOWS.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEM_GRIFF.value,)]
        )

    def test_access_locations_requiring_totem_lucy(self) -> None:
        locations: List[str] = [
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.STRIP_GRUE_FIRE_WATER.value,
            ZorkGrandInquisitorLocations.WE_GOT_A_HIGH_ROLLER.value,
            ZorkGrandInquisitorEvents.VICTORY.value,
        ]

        self.assertAccessDependency(
            locations, [(ZorkGrandInquisitorItems.TOTEM_LUCY.value,)]
        )
