from typing import Dict, List, Set, Tuple, TextIO, Any, Optional
from BaseClasses import Item, Tutorial, ItemClassification
from .Items import get_item_names_per_category
from .Items import item_table, starter_melee_weapons, starter_spells, filler_items, starter_progression_items, pyramid_start_starter_progression_items
from .Locations import get_location_datas, EventId
from .Options import BackwardsCompatiableTimespinnerOptions, Toggle, BossRandoType
from .PreCalculatedWeights import PreCalculatedWeights
from .Regions import create_regions_and_locations
from worlds.AutoWorld import World, WebWorld
import logging

class TimespinnerWebWorld(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Timespinner randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jarno"]
    )

    setup_de = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["Grrmo", "Fynxes", "Blaze0168"]
    )

    tutorials = [setup, setup_de]

class TimespinnerWorld(World):
    """
    Timespinner is a beautiful metroidvania inspired by classic 90s action-platformers.
    Travel back in time to change fate itself. Join timekeeper Lunais on her quest for revenge against the empire that killed her family.
    """
    options_dataclass = BackwardsCompatiableTimespinnerOptions
    options: BackwardsCompatiableTimespinnerOptions
    game = "Timespinner"
    topology_present = True
    web = TimespinnerWebWorld()
    required_client_version = (0, 4, 2)
    ut_can_gen_without_yaml = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_location_datas(-1, None, None)}
    item_name_groups = get_item_names_per_category()

    precalculated_weights: PreCalculatedWeights

    def generate_early(self) -> None:
        self.options.handle_backward_compatibility()

        self.precalculated_weights = PreCalculatedWeights(self.options, self.random)

        # in generate_early the start_inventory isnt copied over to precollected_items yet, so we can still modify the options directly
        if self.options.start_inventory.value.pop("Meyef", 0) > 0:
            self.options.start_with_meyef.value = Toggle.option_true
        if self.options.start_inventory.value.pop("Talaria Attachment", 0) > 0:
            self.options.quick_seed.value = Toggle.option_true
        if self.options.start_inventory.value.pop("Jewelry Box", 0) > 0:
            self.options.start_with_jewelry_box.value = Toggle.option_true

        self.interpret_slot_data(None)

        if self.options.quick_seed:
            self.multiworld.push_precollected(self.create_item("Talaria Attachment"))

    def create_regions(self) -> None: 
        create_regions_and_locations(self.multiworld, self.player, self.options, self.precalculated_weights)

    def create_items(self) -> None: 
        self.create_and_assign_event_items()

        excluded_items: Set[str] = self.get_excluded_items()

        self.assign_starter_items(excluded_items)
        self.place_first_progression_item(excluded_items)

        self.multiworld.itempool += self.get_item_pool(excluded_items)

    def set_rules(self) -> None:
        final_boss: str
        if self.options.dad_percent:
            final_boss = "Killed Emperor"
        else:
            final_boss = "Killed Nightmare"

        self.multiworld.completion_condition[self.player] = lambda state: state.has(final_boss, self.player) 

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            # options
            "StartWithJewelryBox": self.options.start_with_jewelry_box.value,
            "DownloadableItems": self.options.downloadable_items.value,
            "EyeSpy": self.options.eye_spy.value,
            "StartWithMeyef": self.options.start_with_meyef.value,
            "QuickSeed": self.options.quick_seed.value,
            "SpecificKeycards": self.options.specific_keycards.value,
            "Inverted": self.options.inverted.value,
            "GyreArchives": self.options.gyre_archives.value,
            "Cantoran": self.options.cantoran.value,
            "LoreChecks": self.options.lore_checks.value,
            "BossRando": self.options.boss_rando.value,
            "BossRandoType": self.options.boss_rando_type.value,
            "BossRandoOverrides": self.precalculated_weights.boss_rando_overrides,
            "EnemyRando": self.options.enemy_rando.value,
            "DamageRando": self.options.damage_rando.value,
            "DamageRandoOverrides": self.options.damage_rando_overrides.value,
            "HpCap": self.options.hp_cap.value,
            "AuraCap": self.options.aura_cap.value,
            "LevelCap": self.options.level_cap.value,
            "ExtraEarringsXP": self.options.extra_earrings_xp.value,
            "BossHealing": self.options.boss_healing.value,
            "ShopFill": self.options.shop_fill.value,
            "ShopWarpShards": self.options.shop_warp_shards.value,
            "ShopMultiplier": self.options.shop_multiplier.value,
            "LootPool": self.options.loot_pool.value,
            "DropRateCategory": self.options.drop_rate_category.value,
            "FixedDropRate": self.options.fixed_drop_rate.value,
            "LootTierDistro": self.options.loot_tier_distro.value,
            "ShowBestiary": self.options.show_bestiary.value,
            "ShowDrops": self.options.show_drops.value,
            "EnterSandman": self.options.enter_sandman.value,
            "DadPercent": self.options.dad_percent.value,
            "RisingTides": self.options.rising_tides.value,
            "UnchainedKeys": self.options.unchained_keys.value,
            "PresentAccessWithWheelAndSpindle": self.options.back_to_the_future.value,
            "PrismBreak": self.options.prism_break.value,
            "LockKeyAmadeus": self.options.lock_key_amadeus.value,
            "RiskyWarps": self.options.risky_warps.value,
            "PyramidStart": self.options.pyramid_start.value,
            "GateKeep": self.options.gate_keep.value,
            "RoyalRoadblock": self.options.royal_roadblock.value,
            "PureTorcher": self.options.pure_torcher.value,
            "FindTheFlame": self.options.find_the_flame.value,
            "Traps": self.options.traps.value,
            "DeathLink": self.options.death_link.value,
            "StinkyMaw": True,
            # data
            "PersonalItems": self.get_personal_items(),
            "PyramidKeysGate": self.precalculated_weights.pyramid_keys_unlock,
            "PresentGate": self.precalculated_weights.present_key_unlock,
            "PastGate": self.precalculated_weights.past_key_unlock,
            "TimeGate": self.precalculated_weights.time_key_unlock,
            # rising tides
            "Basement": int(self.precalculated_weights.flood_basement) + \
                                    int(self.precalculated_weights.flood_basement_high),
            "Xarion": self.precalculated_weights.flood_xarion,
            "Maw": self.precalculated_weights.flood_maw,
            "PyramidShaft": self.precalculated_weights.flood_pyramid_shaft,
            "BackPyramid": self.precalculated_weights.flood_pyramid_back,
            "CastleMoat": self.precalculated_weights.flood_moat,
            "CastleCourtyard": self.precalculated_weights.flood_courtyard,
            "LakeDesolation": self.precalculated_weights.flood_lake_desolation,
            "DryLakeSerene": not self.precalculated_weights.flood_lake_serene,
            "LakeSereneBridge": self.precalculated_weights.flood_lake_serene_bridge,
            "Lab": self.precalculated_weights.flood_lab
        }
    
    def interpret_slot_data(self, slot_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Used by Universal Tracker to correctly rebuild state"""

        if not slot_data \
            and hasattr(self.multiworld, "re_gen_passthrough") \
            and isinstance(self.multiworld.re_gen_passthrough, dict) \
            and "Timespinner" in self.multiworld.re_gen_passthrough:
                slot_data = self.multiworld.re_gen_passthrough["Timespinner"]

        if not slot_data:
            return None
        
        self.options.start_with_jewelry_box.value = slot_data["StartWithJewelryBox"]
        self.options.downloadable_items.value = slot_data["DownloadableItems"]
        self.options.eye_spy.value = slot_data["EyeSpy"]
        self.options.start_with_meyef.value = slot_data["StartWithMeyef"]
        self.options.quick_seed.value = slot_data["QuickSeed"]
        self.options.specific_keycards.value = slot_data["SpecificKeycards"]
        self.options.inverted.value = slot_data["Inverted"]
        self.options.gyre_archives.value = slot_data["GyreArchives"]
        self.options.cantoran.value = slot_data["Cantoran"]
        self.options.lore_checks.value = slot_data["LoreChecks"]
        self.options.boss_rando.value = slot_data["BossRando"]
        self.options.boss_rando_type.value = slot_data["BossRandoType"]
        self.precalculated_weights.boss_rando_overrides = slot_data["BossRandoOverrides"]
        self.options.damage_rando.value = slot_data["DamageRando"]
        self.options.damage_rando_overrides.value = slot_data["DamageRandoOverrides"]
        self.options.hp_cap.value = slot_data["HpCap"]
        self.options.level_cap.value = slot_data["LevelCap"]
        self.options.extra_earrings_xp.value = slot_data["ExtraEarringsXP"]
        self.options.boss_healing.value = slot_data["BossHealing"]
        self.options.shop_fill.value = slot_data["ShopFill"]
        self.options.shop_warp_shards.value = slot_data["ShopWarpShards"]
        self.options.shop_multiplier.value = slot_data["ShopMultiplier"]
        self.options.loot_pool.value = slot_data["LootPool"]
        self.options.drop_rate_category.value = slot_data["DropRateCategory"]
        self.options.fixed_drop_rate.value = slot_data["FixedDropRate"]
        self.options.loot_tier_distro.value = slot_data["LootTierDistro"]
        self.options.show_bestiary.value = slot_data["ShowBestiary"]
        self.options.show_drops.value = slot_data["ShowDrops"]
        self.options.enter_sandman.value = slot_data["EnterSandman"]
        self.options.dad_percent.value = slot_data["DadPercent"]
        self.options.rising_tides.value = slot_data["RisingTides"]
        self.options.unchained_keys.value = slot_data["UnchainedKeys"]
        self.options.back_to_the_future.value = slot_data["PresentAccessWithWheelAndSpindle"]
        self.options.prism_break.value = slot_data["PrismBreak"]
        self.options.traps.value = slot_data["Traps"]
        self.options.death_link.value = slot_data["DeathLink"]
        # Readonly slot_data["StinkyMaw"]
        # data
        # Readonly slot_data["PersonalItems"]
        self.precalculated_weights.pyramid_keys_unlock = slot_data["PyramidKeysGate"]
        self.precalculated_weights.present_key_unlock = slot_data["PresentGate"]
        self.precalculated_weights.past_key_unlock = slot_data["PastGate"]
        self.precalculated_weights.time_key_unlock = slot_data["TimeGate"]
        # rising tides
        if (slot_data["Basement"] > 0):
            self.precalculated_weights.flood_basement = True
        if (slot_data["Basement"] == 2):
            self.precalculated_weights.flood_basement_high = True
        self.precalculated_weights.flood_xarion = slot_data["Xarion"]
        self.precalculated_weights.flood_maw = slot_data["Maw"]
        self.precalculated_weights.flood_pyramid_shaft = slot_data["PyramidShaft"]
        self.precalculated_weights.flood_pyramid_back = slot_data["BackPyramid"]
        self.precalculated_weights.flood_moat = slot_data["CastleMoat"]
        self.precalculated_weights.flood_courtyard = slot_data["CastleCourtyard"]
        self.precalculated_weights.flood_lake_desolation = slot_data["LakeDesolation"]
        self.precalculated_weights.flood_lake_serene = not slot_data["DryLakeSerene"]
        self.precalculated_weights.flood_lake_serene_bridge = slot_data["LakeSereneBridge"]
        self.precalculated_weights.flood_lab = slot_data["Lab"]

        return slot_data

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.unchained_keys:
            spoiler_handle.write(f'Modern Warp Beacon unlock:       {self.precalculated_weights.present_key_unlock}\n')
            spoiler_handle.write(f'Timeworn Warp Beacon unlock:     {self.precalculated_weights.past_key_unlock}\n')

            if self.options.enter_sandman:
                spoiler_handle.write(f'Mysterious Warp Beacon unlock:   {self.precalculated_weights.time_key_unlock}\n')
        else:
            spoiler_handle.write(f'Twin Pyramid Keys unlock:        {self.precalculated_weights.pyramid_keys_unlock}\n')

        if self.options.boss_rando.value and self.options.boss_rando_type.value == BossRandoType.option_manual:
            spoiler_handle.write(f'Selected bosses:                 {self.precalculated_weights.boss_rando_overrides}\n')

        if self.options.rising_tides:
            flooded_areas: List[str] = []

            if self.precalculated_weights.flood_basement:
                if self.precalculated_weights.flood_basement_high:
                    flooded_areas.append("Castle Basement")
                else:
                    flooded_areas.append("Castle Basement (Savepoint available)")
            if self.precalculated_weights.flood_xarion:
                flooded_areas.append("Xarion (boss)")
            if self.precalculated_weights.flood_maw:
                flooded_areas.append("Maw (caves + boss)")
            if self.precalculated_weights.flood_pyramid_shaft:
                flooded_areas.append("Ancient Pyramid Shaft")
            if self.precalculated_weights.flood_pyramid_back:
                flooded_areas.append("Sandman\\Nightmare (boss)")
            if self.precalculated_weights.flood_moat:
                flooded_areas.append("Castle Ramparts Moat")
            if self.precalculated_weights.flood_courtyard:
                flooded_areas.append("Castle Courtyard")
            if self.precalculated_weights.flood_lake_desolation:
                flooded_areas.append("Lake Desolation")
            if self.precalculated_weights.flood_lake_serene:
                flooded_areas.append("Lake Serene")
            if self.precalculated_weights.flood_lake_serene_bridge:
                flooded_areas.append("Lake Serene Bridge")
            if self.precalculated_weights.flood_lab:
                flooded_areas.append("Lab")

            if len(flooded_areas) == 0:
                flooded_areas_string: str = "None"
            else:
                flooded_areas_string: str = ", ".join(flooded_areas)

            spoiler_handle.write(f'Flooded Areas:                   {flooded_areas_string}\n')

        if self.options.has_replaced_options:
            warning = \
                f"NOTICE: Timespinner options for player '{self.player_name}' were renamed from PascalCase to snake_case, " \
                "please update your yaml"

            spoiler_handle.write("\n")
            spoiler_handle.write(warning)
            logging.warning(warning)

    def create_item(self, name: str) -> Item:
        data = item_table[name]

        if data.useful:
            classification = ItemClassification.useful
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler
            
        item = Item(name, classification, data.code, self.player)

        if not item.advancement:
            return item

        if name == 'Tablet' and not self.options.downloadable_items:
            item.classification = ItemClassification.filler
        elif name == 'Library Keycard V' and not (self.options.downloadable_items or self.options.pure_torcher):
            item.classification = ItemClassification.filler
        elif name == 'Oculus Ring' and not self.options.eye_spy:
            item.classification = ItemClassification.filler
        elif (name == 'Kobo' or name == 'Merchant Crow') and not self.options.gyre_archives:
            item.classification = ItemClassification.filler
        elif name in {"Timeworn Warp Beacon", "Modern Warp Beacon", "Mysterious Warp Beacon"} \
                and not self.options.unchained_keys:
            item.classification = ItemClassification.filler
        elif name in {"Laser Access A", "Laser Access I", "Laser Access M"} \
                and not self.options.prism_break:
            item.classification = ItemClassification.filler
        elif name in {"Lab Access Genza", "Lab Access Experiment", "Lab Access Research", "Lab Access Dynamo"} \
                and not self.options.lock_key_amadeus:
            item.classification = ItemClassification.filler
        elif name == "Drawbridge Key" and not self.options.gate_keep: 
            item.classification = ItemClassification.filler
        elif name == "Cube of Bodie" and not self.options.find_the_flame: 
            item.classification = ItemClassification.filler

        return item

    def get_filler_item_name(self) -> str:
        trap_chance: int = self.options.trap_chance.value
        enabled_traps: List[str] = self.options.traps.value

        if self.random.random() < (trap_chance / 100) and enabled_traps:
            return self.random.choice(enabled_traps)
        else:
            return self.random.choice(filler_items) 

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()

        if self.options.start_with_jewelry_box:
            excluded_items.add('Jewelry Box')
        if self.options.start_with_meyef:
            excluded_items.add('Meyef')
        if self.options.quick_seed:
            excluded_items.add('Talaria Attachment')

        if self.options.unchained_keys:
            excluded_items.add('Twin Pyramid Key')

            if not self.options.enter_sandman:
                excluded_items.add('Mysterious Warp Beacon')
        else:
            excluded_items.add('Timeworn Warp Beacon')
            excluded_items.add('Modern Warp Beacon')
            excluded_items.add('Mysterious Warp Beacon')

        if not self.options.prism_break:
            excluded_items.add('Laser Access A')
            excluded_items.add('Laser Access I')
            excluded_items.add('Laser Access M')

        if not self.options.lock_key_amadeus:
            excluded_items.add('Lab Access Genza')
            excluded_items.add('Lab Access Experiment')
            excluded_items.add('Lab Access Research')
            excluded_items.add('Lab Access Dynamo')

        if not self.options.gate_keep:
            excluded_items.add('Drawbridge Key')

        if not self.options.find_the_flame:
            excluded_items.add('Cube of Bodie')

        for item in self.multiworld.precollected_items[self.player]:
            if item.name not in self.item_name_groups['UseItem']:
                excluded_items.add(item.name)

        return excluded_items

    def assign_starter_items(self, excluded_items: Set[str]) -> None:
        non_local_items: Set[str] = self.options.non_local_items.value
        local_items: Set[str] = self.options.local_items.value

        local_starter_melee_weapons = tuple(item for item in starter_melee_weapons if
                                            item in local_items or not item in non_local_items)
        if not local_starter_melee_weapons:
            if 'Plasma Orb' in non_local_items:
                raise Exception("Atleast one melee orb must be local")
            else:
                local_starter_melee_weapons = ('Plasma Orb',)

        local_starter_spells = tuple(item for item in starter_spells if
                                     item in local_items or not item in non_local_items)
        if not local_starter_spells:
            if 'Lightwall' in non_local_items:
                raise Exception("Atleast one spell must be local")
            else:
                local_starter_spells = ('Lightwall',)

        self.assign_starter_item(excluded_items, 'Tutorial: Yo Momma 1', local_starter_melee_weapons)
        self.assign_starter_item(excluded_items, 'Tutorial: Yo Momma 2', local_starter_spells)

    def assign_starter_item(self, excluded_items: Set[str], location: str, item_list: Tuple[str, ...]) -> None:
        item_name = self.random.choice(item_list)

        self.place_locked_item(excluded_items, location, item_name)

    def place_first_progression_item(self, excluded_items: Set[str]) -> None:
        if (self.options.quick_seed or self.options.inverted or self.precalculated_weights.flood_lake_desolation) \
        and not self.options.pyramid_start:
            return

        enabled_starter_progression_items = pyramid_start_starter_progression_items if self.options.pyramid_start else starter_progression_items

        for item_name in self.options.start_inventory.value.keys():
            if item_name in enabled_starter_progression_items:
                return

        local_starter_progression_items = tuple(
            item for item in enabled_starter_progression_items 
                if item not in excluded_items and item not in self.options.non_local_items.value)

        if not local_starter_progression_items:
            return

        progression_item = self.random.choice(local_starter_progression_items)

        self.multiworld.local_early_items[self.player][progression_item] = 1

    def place_locked_item(self, excluded_items: Set[str], location: str, item: str) -> None:
        excluded_items.add(item)

        item = self.create_item(item)

        self.multiworld.get_location(location, self.player).place_locked_item(item)

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                for _ in range(data.count):
                    item = self.create_item(name)
                    pool.append(item)

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.create_item(self.get_filler_item_name())
            pool.append(item)

        return pool

    def create_and_assign_event_items(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if location.address == EventId:
                item = Item(location.name, ItemClassification.progression, EventId, self.player)
                location.place_locked_item(item)

    def get_personal_items(self) -> Dict[int, int]:
        personal_items: Dict[int, int] = {}

        for location in self.multiworld.get_locations(self.player):
            if location.address and location.item and location.item.code and location.item.player == self.player:
                personal_items[location.address] = location.item.code

        return personal_items
